import random
from dictionary import load_list
from filters import valid
from scoring import score
from config import MIN_LENGTH,MAX_LENGTH
def normalise_name(n): return n.capitalize()
def generate_candidates(count):
 p=load_list("prefixes.txt");m=load_list("middles.txt");s=load_list("suffixes.txt");b=load_list("banned.txt")
 out=[];rej=[];seen=set()
 pats=[("p+m+s",lambda:random.choice(p)+random.choice(m)+random.choice(s)),
 ("p+s",lambda:random.choice(p)+random.choice(s)),
 ("p+m+m+s",lambda:random.choice(p)+random.choice(m)+random.choice(m)+random.choice(s))]
 while len(out)<count:
  pat,f=random.choice(pats);n=f()
  ok,r=valid(n,b,MIN_LENGTH,MAX_LENGTH)
  if not ok: rej.append((n,r));continue
  if n in seen: continue
  seen.add(n);out.append((normalise_name(n),score(n),len(n),pat))
 out.sort(key=lambda x:x[1],reverse=True)
 return out,rej
