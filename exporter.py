import csv


def write(path,rows):
 with open(path,"w",newline="") as f:
  w=csv.writer(f)
  w.writerow([
   "rank","name","score","length","pattern",
   "meaning_score","rhythm_score","memorability_score",
   "warmth_score","professionalism_score","overall_score",
   "territory","source_words",
  ])
  [w.writerow(r) for r in rows]


def write_rejected(path,rows):
 with open(path,"w",newline="") as f:
  w=csv.writer(f);w.writerow(["candidate","reason"]);w.writerows(rows)
