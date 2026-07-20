import re
def valid(name,banned,minl,maxl):
 n=name.lower()
 if len(n)<minl or len(n)>maxl:return False,"length"
 if any(b in n for b in banned):return False,"banned"
 if re.search(r"[0-9 -]",n):return False,"chars"
 if re.search(r"[aeiou]{3,}",n):return False,"vowels"
 if re.search(r"[^aeiou]{4,}",n):return False,"consonants"
 if re.search(r"(.)\1\1",n):return False,"repeat"
 return True,"ok"
