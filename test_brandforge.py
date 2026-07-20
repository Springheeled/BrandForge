import csv
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from derivation import iter_brand_candidates
from dictionary import load_list
from exporter import HEADERS,write,write_top_30
from filters import valid
from generator import generate_all_candidates,generate_candidates
from scoring import quality_gate,score,score_candidate
from territories import TERRITORIES,iter_candidates


class MeaningEngineTests(unittest.TestCase):
 def test_top_100_is_meaning_led_and_fully_scored(self):
  rows,_=generate_candidates(100)
  self.assertEqual(len(rows),100)
  self.assertEqual(len({row[0].lower() for row in rows}),100)
  for row in rows:
   self.assertEqual(len(row),21)
   self.assertIn(row[3],{
    "source","transparent_compound","distilled","blend","rhythmic","pac",
   })
   for value in row[4:10]+row[12:17]:
    self.assertGreaterEqual(value,0)
    self.assertLessEqual(value,100)
   self.assertTrue(row[10])
   self.assertTrue(row[11])
   self.assertTrue(row[17])
   self.assertTrue(row[18])

 def test_distilled_generation_is_deterministic(self):
  first=[
   (seed.name,seed.territory.name,seed.sources,seed.transformation)
   for seed in iter_brand_candidates()
   if seed.generation_mode=="distilled"
  ]
  second=[
   (seed.name,seed.territory.name,seed.sources,seed.transformation)
   for seed in iter_brand_candidates()
   if seed.generation_mode=="distilled"
  ]
  self.assertEqual(first,second)
  self.assertGreater(len(first),20)

 def test_every_candidate_has_semantic_provenance(self):
  territories={territory.name for territory in TERRITORIES}
  for seed in iter_brand_candidates():
   self.assertIn(seed.territory.name,territories)
   self.assertTrue(seed.sources)
   self.assertTrue(all(source for source in seed.sources))
   self.assertTrue(seed.transformation)
   self.assertTrue(seed.rationale)
   if seed.generation_mode in ("distilled","blend"):
    self.assertNotEqual(seed.name,"".join(seed.sources))

 def test_meaningless_mutation_fails_semantic_gate(self):
  scores=score_candidate(
   "zovixa",TERRITORIES[0],"blend",("steady","guide"),
   "replace both sources with unrelated sounds",
  )
  accepted,reason=quality_gate(scores)
  self.assertFalse(accepted)
  self.assertEqual(reason,"semantic_retention")
  self.assertLess(scores["semantic_retention"],70)

 def test_generic_dictionary_word_is_penalised(self):
  source=score_candidate(
   "secure",TERRITORIES[9],"source",("secure",),"unchanged source word",
  )
  distilled=score_candidate(
   "secura",TERRITORIES[9],"distilled",("secure",),
   "replace terminal -e with -a",
  )
  self.assertGreaterEqual(source["penalty"],15)
  self.assertIn("generic dictionary word",source["weaknesses"])
  self.assertGreater(distilled["distinctiveness"],source["distinctiveness"])

 def test_transparent_compound_is_penalised(self):
  transparent=score_candidate(
   "clearpath",TERRITORIES[3],"transparent_compound",
   ("clear","path"),"join complete source words",
  )
  rhythmic=score_candidate(
   "clearpath",TERRITORIES[3],"rhythmic",
   ("clear","pathway"),"pair short rhythmic roots clear + path",
  )
  self.assertGreater(transparent["penalty"],rhythmic["penalty"])
  self.assertIn("obvious transparent compound",transparent["weaknesses"])
  self.assertGreater(rhythmic["overall"],transparent["overall"])

 def test_formulaic_suffix_and_sector_resemblance_are_penalised(self):
  trendy=score_candidate(
   "flowify",TERRITORIES[2],"distilled",("fluent",),
   "formulaic suffix",
  )
  fleet=score_candidate(
   "fleetway",TERRITORIES[5],"blend",("route","pathway"),
   "blend semantic roots",
  )
  self.assertTrue(any("formulaic -ify" in item for item in trendy["weaknesses"]))
  self.assertTrue(any("vehicle fleet" in item for item in fleet["weaknesses"]))

 def test_pac_candidates_remain_a_minority(self):
  seeds=list(iter_brand_candidates())
  pac_seeds=[seed for seed in seeds if seed.generation_mode=="pac"]
  rows,_=generate_candidates(100)
  pac_rows=[row for row in rows if row[3]=="pac"]
  self.assertGreater(len(pac_seeds),0)
  self.assertLess(len(pac_seeds),len(seeds)*.10)
  self.assertGreater(len(pac_rows),0)
  self.assertLessEqual(len(pac_rows),10)

 def test_duplicate_removal_is_case_insensitive(self):
  rows,_=generate_all_candidates()
  names=[row[0].lower() for row in rows]
  self.assertEqual(len(names),len(set(names)))
  self.assertEqual(names.count("anchora"),1)

 def test_top_100_ordering_is_stable(self):
  first,_=generate_candidates(100)
  second,_=generate_candidates(100)
  self.assertEqual(first,second)

 def test_spelling_and_phonetic_quality_gates(self):
  banned=load_list("banned.txt")
  self.assertEqual(valid("bcrane",banned,5,12),(False,"pronunciation"))
  self.assertEqual(valid("aeiron",banned,5,12),(False,"vowels"))
  self.assertEqual(valid("striven",banned,5,12),(True,"ok"))
  rows,_=generate_all_candidates()
  self.assertTrue(all(row[13]>=65 for row in rows))
  self.assertTrue(all(row[14]>=68 for row in rows))
  self.assertTrue(all(row[15]>=70 for row in rows))

 def test_top_30_is_not_dominated_by_low_distinction_modes(self):
  rows,_=generate_candidates(100)
  modes=Counter(row[3] for row in rows[:30])
  self.assertEqual(modes["source"],0)
  self.assertEqual(modes["transparent_compound"],0)
  self.assertLessEqual(modes["pac"],3)
  self.assertLessEqual(modes["distilled"],20)
  source_frequency=Counter(
   source
   for row in rows[:30]
   for source in row[11].split("+")
  )
  self.assertLessEqual(max(source_frequency.values()),3)

 def test_original_pronunciation_and_territory_contracts_remain(self):
  self.assertEqual(score("monzo"),95)
  self.assertEqual(len({territory.name for territory in TERRITORIES}),12)
  self.assertTrue(all(tuple(iter_candidates())))

 def test_csv_and_markdown_exports_include_sprint_2_provenance(self):
  rows,_=generate_candidates(3)
  with tempfile.TemporaryDirectory() as directory:
   csv_path=Path(directory)/"top_100.csv"
   md_path=Path(directory)/"top_30.md"
   write(csv_path,[(index+1,*row) for index,row in enumerate(rows)])
   write_top_30(md_path,rows)
   with csv_path.open(newline="",encoding="utf-8") as handle:
    exported=list(csv.reader(handle))
   report=md_path.read_text(encoding="utf-8")
  self.assertEqual(exported[0],HEADERS)
  self.assertEqual(len(exported),4)
  self.assertIn("Score breakdown",report)
  self.assertIn("Generation method",report)
  self.assertIn("Weaknesses",report)
