from generator import generate_candidates
from exporter import write,write_rejected
from config import OUTPUT_COUNT
from pathlib import Path
print("BrandForge Phase 1\nGenerating candidates...")
rows,rej=generate_candidates(OUTPUT_COUNT)
out=Path("output");out.mkdir(exist_ok=True)
write(out/"candidates.csv",[(i+1,*r) for i,r in enumerate(rows)])
write_rejected(out/"rejected.csv",rej)
print(f"Generated {len(rows)} unique names.")
print("Saved to output/candidates.csv")
