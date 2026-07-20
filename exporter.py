import csv


HEADERS=[
 "rank","name","score","length","pattern",
 "meaning_score","rhythm_score","memorability_score",
 "warmth_score","professionalism_score","overall_score",
 "territory","source_words","distinctiveness_score",
 "spelling_confidence_score","phonetic_naturalness_score",
 "semantic_retention_score","brand_rhythm_score",
 "transformation","semantic_rationale","weaknesses","penalty",
]


def write(path,rows):
 with open(path,"w",newline="",encoding="utf-8") as f:
  w=csv.writer(f)
  w.writerow(HEADERS)
  w.writerows(rows)


def write_rejected(path,rows):
 with open(path,"w",newline="",encoding="utf-8") as f:
  w=csv.writer(f);w.writerow(["candidate","reason"]);w.writerows(rows)


def _markdown(value):
 return str(value).replace("|","\\|").replace("\n"," ")


def write_top_30(path,rows):
 lines=[
  "# BrandForge Top 30",
  "",
  "Meaning-led candidates ranked for distinctiveness, clarity and long-term brand potential.",
  "",
  "| Rank | Candidate | Overall | Score breakdown | Source concept | Generation method | Rationale | Weaknesses |",
  "|---:|---|---:|---|---|---|---|---|",
 ]
 for rank,row in enumerate(rows[:30],1):
  breakdown=(
   f"meaning {row[4]}; rhythm {row[5]}; memory {row[6]}; "
   f"warmth {row[7]}; professional {row[8]}; distinctive {row[12]}; "
   f"spelling {row[13]}; phonetic {row[14]}; retention {row[15]}; "
   f"brand rhythm {row[16]}"
  )
  method=f"{row[3]}: {row[17]}"
  lines.append(
   f"| {rank} | **{_markdown(row[0])}** | {row[9]} | "
   f"{_markdown(breakdown)} | {_markdown(row[10]+': '+row[11])} | "
   f"{_markdown(method)} | {_markdown(row[18])} | {_markdown(row[19])} |"
  )
 path.write_text("\n".join(lines)+"\n",encoding="utf-8")
