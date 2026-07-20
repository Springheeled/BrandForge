from dictionary import load_list
from filters import valid
from scoring import quality_gate,score_candidate
from config import MIN_LENGTH,MAX_LENGTH
from derivation import iter_brand_candidates


GENERATION_MODES={
 "source","transparent_compound","distilled","blend","rhythmic","pac",
}


def normalise_name(n): return n.capitalize()


def _candidate_row(seed,scores):
 return (
  normalise_name(seed.name),
  scores["pronunciation"],
  len(seed.name),
  seed.generation_mode,
  scores["meaning"],
  scores["rhythm"],
  scores["memorability"],
  scores["warmth"],
  scores["professionalism"],
  scores["overall"],
  seed.territory.name,
  "+".join(seed.sources),
  scores["distinctiveness"],
  scores["spelling_confidence"],
  scores["phonetic_naturalness"],
  scores["semantic_retention"],
  scores["brand_rhythm"],
  seed.transformation,
  seed.rationale,
  "; ".join(scores["weaknesses"]) or "none detected",
  scores["penalty"],
 )


def generate_all_candidates():
 b=load_list("banned.txt")
 out={}
 rejected=[]
 for seed in iter_brand_candidates():
  name=seed.name.lower()
  if seed.generation_mode not in GENERATION_MODES:
   rejected.append((name,"generation_mode"))
   continue
  if not seed.sources or not seed.transformation or not seed.rationale:
   rejected.append((name,"semantic_provenance"))
   continue
  if seed.generation_mode in ("distilled","blend") and name=="".join(seed.sources):
   rejected.append((name,"meaningless_mutation"))
   continue
  ok,reason=valid(name,b,MIN_LENGTH,MAX_LENGTH)
  if not ok:
   rejected.append((name,reason))
   continue
  scores=score_candidate(
   name,seed.territory,seed.generation_mode,seed.sources,
   seed.transformation,seed.weaknesses,seed.variant_order,
  )
  ok,reason=quality_gate(scores)
  if not ok:
   rejected.append((name,reason))
   continue
  row=_candidate_row(seed,scores)
  existing=out.get(name)
  if existing is None or row[9]>existing[9]:
   out[name]=row
 rows=sorted(
  out.values(),
  key=lambda row:(-row[9],-row[12],-row[16],row[0].lower()),
 )
 return rows,rejected


def generate_candidates(count):
 rows,rejected=generate_all_candidates()
 selected=[]
 pac_limit=max(1,count//10)
 pac_count=0
 for row in rows:
  if row[3]=="pac":
   if pac_count>=pac_limit:
    continue
   pac_count+=1
  selected.append(row)
  if len(selected)>=count:
   break
 return selected,rejected
