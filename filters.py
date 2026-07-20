import re


NEGATIVE_BRITISH=("naff","dodgy","pants","tosser","wank","knob","crap","shag","slag")
NATURAL_OPENING_CLUSTERS=("str","spr","scr","thr","chr","sch","spl")


def valid(name,banned,minl,maxl):
 n=name.lower()
 if len(n)<minl or len(n)>maxl:return False,"length"
 if any(b in n for b in banned):return False,"banned"
 if any(term in n for term in NEGATIVE_BRITISH):return False,"negative"
 if re.search(r"[0-9 -]",n):return False,"chars"
 if re.search(r"[aeiou]{3,}",n):return False,"vowels"
 if re.search(r"[^aeiouy]{4,}",n):return False,"consonants"
 if re.search(r"(.)\1\1",n):return False,"repeat"
 if re.search(r"(.{2})\1",n):return False,"repeated_pair"
 if not re.search(r"[aeiouy]",n):return False,"pronunciation"
 if re.search(r"q(?!u)",n):return False,"pronunciation"
 opening=re.match(r"^[^aeiouy]{3}",n)
 if opening and opening.group(0) not in NATURAL_OPENING_CLUSTERS:
  return False,"pronunciation"
 if n[-1] in "jqv":return False,"pronunciation"
 return True,"ok"
