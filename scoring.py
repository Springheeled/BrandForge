import re
from difflib import SequenceMatcher


V="aeiou"
TRENDY_SUFFIXES=("ly","ify","io","ster","verse","hub","hq")
SECTOR_MARKERS=(
 ("pharmaceutical",("pharm","med","vax","zole","mycin","cillin","exia")),
 ("cryptocurrency",("coin","token","chain","swap","crypto","block")),
 ("gaming",("game","play","quest","arena")),
 ("vehicle fleet",("fleet","track","drive","haul","route")),
 ("toy",("toy","kids","play","pop")),
 ("packaging",("pack","parcel","carton","wrap","ship")),
)


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
 """Retain the Sprint 1 rhythm score."""
 syllables=_syllable_count(name)
 value=score(name)
 if syllables in (2,3): value+=6
 elif syllables>3: value-=8*(syllables-3)
 if name[-1] in V+"y": value+=2
 if len(name) in range(6,9): value+=3
 return _clamp(value)


def memorability_score(name,kind):
 value=72
 if 5<=len(name)<=8: value+=10
 elif len(name) in (9,10): value+=6
 distinct=len(set(name.lower()))/len(name)
 if distinct>=0.7: value+=5
 if kind in ("distilled","blend","rhythmic"): value+=10
 if kind=="pac": value+=5
 if re.search(r"(.)\1",name.lower()): value-=5
 return _clamp(value)


def meaning_score(kind,source_words):
 if kind=="source": return 100
 if kind in ("transparent_compound","compound") and len(source_words)==2: return 96
 if kind=="distilled": return 92
 if kind=="blend": return 88
 if kind=="rhythmic": return 92
 if kind=="pac": return 82
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
 if len(name)>10: value-=6
 if name.endswith(("ify","ster","zilla")): value-=15
 return _clamp(value)


def distinctiveness_score(name,kind):
 bases={
  "source":48,
  "transparent_compound":58,
  "compound":58,
  "distilled":88,
  "blend":92,
  "rhythmic":82,
  "pac":74,
 }
 value=bases.get(kind,50)
 if len(set(name.lower()))/len(name)>=.75: value+=4
 if 6<=len(name)<=9: value+=3
 return _clamp(value)


def spelling_confidence_score(name,kind,transformation):
 bases={
  "source":100,
  "transparent_compound":98,
  "compound":98,
  "distilled":88,
  "blend":80,
  "rhythmic":94,
  "pac":82,
 }
 value=bases.get(kind,70)
 if re.search(r"[^aeiouy]{3}",name.lower()): value-=8
 if re.search(r"[aeiou]{2}",name.lower()): value-=4
 if name[-1] in "jqvx": value-=12
 if "substitut" in transformation: value-=2
 return _clamp(value)


def brand_rhythm_score(name):
 syllables=_syllable_count(name)
 value=66
 if syllables==2: value+=20
 elif syllables==3: value+=16
 elif syllables==1: value+=5
 else: value-=8*(syllables-3)
 if 6<=len(name)<=8: value+=8
 elif len(name) in (9,10): value+=5
 if name[-1] in V+"y": value+=3
 transitions=sum(
  (left in V)!=(right in V)
  for left,right in zip(name.lower(),name.lower()[1:])
 )
 value+=round(8*transitions/max(1,len(name)-1))
 return _clamp(value)


def phonetic_naturalness_score(name):
 value=round(score(name)*.62+brand_rhythm_score(name)*.38)
 if re.search(r"[^aeiouy]{3}",name.lower()): value-=8
 if re.search(r"[aeiou]{2}",name.lower()): value-=3
 if re.search(r"q(?!u)",name.lower()): value-=20
 return _clamp(value)


def semantic_retention_score(name,kind,source_words):
 if kind=="source": return 100
 if kind in ("transparent_compound","compound"): return 98
 ratios=[SequenceMatcher(None,name.lower(),source.lower()).ratio() for source in source_words]
 strongest=max(ratios,default=0)
 if kind=="distilled": return _clamp(70+30*strongest)
 if kind=="blend": return _clamp(55+70*strongest)
 if kind=="rhythmic": return _clamp(70+30*strongest)
 if kind=="pac": return _clamp(60+40*strongest)
 return 0


def _penalty_profile(name,kind,variant_order):
 descriptive_components=("path","way","flow","line","mark","well")
 weaknesses=[]
 penalty=0
 if kind=="source":
  weaknesses.append("generic dictionary word")
  penalty+=15
 if kind in ("transparent_compound","compound"):
  weaknesses.append("obvious transparent compound")
  penalty+=12
 if kind=="rhythmic":
  weaknesses.append("two-part construction may feel descriptive")
  penalty+=4
 if kind=="pac":
  weaknesses.append("PAC may imply packaging")
  penalty+=7
 if variant_order:
  weaknesses.append("secondary variant of the same source root")
  penalty+=variant_order*12
 if kind=="distilled" and name.endswith("a"):
  weaknesses.append("Latinised -a ending may feel formulaic or pharmaceutical")
  penalty+=10
 if kind in ("blend","rhythmic") and any(
  component in name.lower() for component in descriptive_components
 ):
  weaknesses.append("retains an obvious descriptive component")
  penalty+=3
 lower=name.lower()
 for suffix in TRENDY_SUFFIXES:
  if lower.endswith(suffix):
   weaknesses.append(f"formulaic -{suffix} suffix")
   penalty+=10
   break
 for sector,markers in SECTOR_MARKERS:
  if any(marker in lower for marker in markers):
   weaknesses.append(f"may resemble a {sector} brand")
   penalty+=9
   break
 return penalty,weaknesses


def score_candidate(
 name,territory,kind,source_words,transformation="",
 seed_weaknesses=(),variant_order=0,
):
 pronunciation=score(name)
 scores={
  "pronunciation":pronunciation,
  "meaning":meaning_score(kind,source_words),
  "rhythm":rhythm_score(name),
  "memorability":memorability_score(name,kind),
  "warmth":warmth_score(name,territory),
  "professionalism":professionalism_score(name,territory,kind),
  "distinctiveness":distinctiveness_score(name,kind),
  "spelling_confidence":spelling_confidence_score(name,kind,transformation),
  "phonetic_naturalness":phonetic_naturalness_score(name),
  "semantic_retention":semantic_retention_score(name,kind,source_words),
  "brand_rhythm":brand_rhythm_score(name),
 }
 penalty,detected=_penalty_profile(name,kind,variant_order)
 weaknesses=list(seed_weaknesses)
 for weakness in detected:
  if weakness not in weaknesses:
   weaknesses.append(weakness)
 raw=(
  scores["meaning"]*.06+
  scores["rhythm"]*.06+
  scores["memorability"]*.08+
  scores["warmth"]*.06+
  scores["professionalism"]*.10+
  pronunciation*.09+
  scores["distinctiveness"]*.16+
  scores["spelling_confidence"]*.10+
  scores["phonetic_naturalness"]*.10+
  scores["semantic_retention"]*.10+
  scores["brand_rhythm"]*.09
 )
 scores["penalty"]=penalty
 scores["weaknesses"]=tuple(weaknesses)
 scores["overall"]=max(0,min(100,round(raw-penalty,1)))
 return scores


def quality_gate(scores):
 if scores["spelling_confidence"]<65:
  return False,"spelling_confidence"
 if scores["phonetic_naturalness"]<68:
  return False,"phonetic_naturalness"
 if scores["semantic_retention"]<70:
  return False,"semantic_retention"
 return True,"ok"
