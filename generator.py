from dictionary import load_list
from filters import valid
from scoring import score_candidate
from config import MIN_LENGTH,MAX_LENGTH
from territories import iter_candidates


def normalise_name(n): return n.capitalize()


def generate_candidates(count):
 b=load_list("banned.txt")
 out={}
 rej=[]
 for n,territory,kind,sources in iter_candidates():
  ok,r=valid(n,b,MIN_LENGTH,MAX_LENGTH)
  if not ok:
   rej.append((n,r))
   continue
  scores=score_candidate(n,territory,kind,sources)
  row=(
   normalise_name(n),
   scores["pronunciation"],
   len(n),
   "meaning:"+kind,
   scores["meaning"],
   scores["rhythm"],
   scores["memorability"],
   scores["warmth"],
   scores["professionalism"],
   scores["overall"],
   territory.name,
   "+".join(sources),
  )
  existing=out.get(n)
  if existing is None or row[9]>existing[9]:
   out[n]=row
 rows=sorted(
  out.values(),
  key=lambda row:(-row[9],-row[4],-row[6],row[0].lower()),
 )
 return rows[:count],rej
