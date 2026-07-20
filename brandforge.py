from generator import generate_all_candidates,generate_candidates
from exporter import write,write_rejected,write_top_30
from config import OUTPUT_COUNT
from pathlib import Path


print("BrandForge V2\nGenerating distilled brand candidates...")
all_rows,rejected=generate_all_candidates()
top_rows,_=generate_candidates(OUTPUT_COUNT)
out=Path("output")
out.mkdir(exist_ok=True)
write(out/"candidates.csv",[(index+1,*row) for index,row in enumerate(all_rows)])
write(out/"top_100.csv",[(index+1,*row) for index,row in enumerate(top_rows)])
write_top_30(out/"top_30.md",top_rows)
write_rejected(out/"rejected.csv",rejected)
print(f"Generated {len(all_rows)} unique qualified names.")
print(f"Ranked the Top {len(top_rows)}.")
print("Saved to output/candidates.csv, output/top_100.csv and output/top_30.md")
