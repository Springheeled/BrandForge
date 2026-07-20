import re


V="aeiou"


def score(n):
 """Return the original BrandForge pronunciation score."""
 s=100
 for i,c in enumerate(n[:-1]):
  if (c in V)==(n[i+1] in V): s-=2
 s-=abs(len(n)-6)*3
 return max(s,0)


def _clamp(value):
 return max(0,min(100,round(value)))


def _syllable_count(name):
 groups=re.findall(r"[aeiouy]+",name.lower())
 return max(1,len(groups))


def rhythm_score(name):
 """Reward compact names with two or three audible beats."""
 syllables=_syllable_count(name)
 value=score(name)
 if syllables in (2,3): value+=6
 elif syllables>3: value-=8*(syllables-3)
 if name[-1] in V+"y": value+=2
 if len(name) in range(6,9): value+=3
 return _clamp(value)


def memorability_score(name,kind):
 """Estimate recall from length, shape and transparent construction."""
 value=76
 if 5<=len(name)<=8: value+=10
 elif len(name)==9: value+=5
 distinct=len(set(name.lower()))/len(name)
 if distinct>=0.7: value+=5
 if kind=="compound": value+=14
 if re.search(r"(.)\1",name.lower()): value-=5
 return _clamp(value)


def meaning_score(kind,source_words):
 """Score semantic traceability rather than novelty for novelty's sake."""
 if kind=="source":
  return 100
 if kind=="compound" and len(source_words)==2:
  return 94
 return 0


def warmth_score(name,territory):
 value=territory.warmth
 if any(sound in name.lower() for sound in ("calm","kind","well","bloom","harmony","gather")):
  value+=5
 if any(sound in name.lower() for sound in ("cross","ground","firm")):
  value-=3
 return _clamp(value)


def professionalism_score(name,territory,kind):
 value=territory.professionalism
 if kind=="source": value+=2
 if len(name)>9: value-=8
 if name.endswith(("ify","ster","zilla")): value-=15
 return _clamp(value)


def score_candidate(name,territory,kind,source_words):
 pronunciation=score(name)
 scores={
  "pronunciation":pronunciation,
  "meaning":meaning_score(kind,source_words),
  "rhythm":rhythm_score(name),
  "memorability":memorability_score(name,kind),
  "warmth":warmth_score(name,territory),
  "professionalism":professionalism_score(name,territory,kind),
 }
 scores["overall"]=round(
  scores["meaning"]*.28+
  scores["rhythm"]*.17+
  scores["memorability"]*.18+
  scores["warmth"]*.12+
  scores["professionalism"]*.15+
  pronunciation*.10,
  1,
 )
 return scores
