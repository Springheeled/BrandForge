from pathlib import Path
def load_list(name):
 p=Path(__file__).parent/"data"/name
 return [l.strip().lower() for l in p.read_text().splitlines() if l.strip() and not l.strip().startswith("#")]
