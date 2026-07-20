V="aeiou"
def score(n):
 s=100
 for i,c in enumerate(n[:-1]):
  if (c in V)==(n[i+1] in V): s-=2
 s-=abs(len(n)-6)*3
 return max(s,0)
