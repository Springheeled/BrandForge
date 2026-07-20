import csv
import tempfile
import unittest
from pathlib import Path

from exporter import write
from generator import generate_candidates
from scoring import score
from territories import TERRITORIES,iter_candidates


PROHIBITED_SUBSTRINGS=(
 "warehouse","logistics","tech","solutions","systems",
 "packaging","shipping","sales",
)


class MeaningEngineTests(unittest.TestCase):
 def test_top_100_is_meaning_led_and_fully_scored(self):
  rows,_=generate_candidates(100)
  self.assertEqual(len(rows),100)
  self.assertEqual(len({row[0].lower() for row in rows}),100)
  for row in rows:
   self.assertEqual(len(row),12)
   self.assertTrue(row[3].startswith("meaning:"))
   self.assertGreaterEqual(row[4],94)
   for value in row[4:10]:
    self.assertGreaterEqual(value,0)
    self.assertLessEqual(value,100)
   self.assertTrue(row[10])
   self.assertTrue(row[11])

 def test_generation_is_deterministic(self):
  first,_=generate_candidates(100)
  second,_=generate_candidates(100)
  self.assertEqual(first,second)

 def test_prohibited_categories_are_not_generated(self):
  rows,_=generate_candidates(100)
  for row in rows:
   name=row[0].lower()
   self.assertNotEqual(name,"ai")
   self.assertFalse(any(term in name for term in PROHIBITED_SUBSTRINGS),name)

 def test_every_candidate_has_meaning_provenance(self):
  territories={territory.name for territory in TERRITORIES}
  self.assertEqual(len(territories),12)
  for candidate,territory,kind,sources in iter_candidates():
   self.assertIn(territory.name,territories)
   self.assertIn(kind,("source","compound"))
   self.assertEqual(candidate,"".join(sources))
   self.assertTrue(all(source for source in sources))

 def test_original_pronunciation_score_is_retained(self):
  self.assertEqual(score("monzo"),95)

 def test_csv_keeps_original_columns_and_adds_new_scores(self):
  rows,_=generate_candidates(2)
  with tempfile.TemporaryDirectory() as directory:
   path=Path(directory)/"candidates.csv"
   write(path,[(index+1,*row) for index,row in enumerate(rows)])
   with path.open(newline="") as handle:
    exported=list(csv.reader(handle))
  self.assertEqual(
   exported[0],
   [
    "rank","name","score","length","pattern",
    "meaning_score","rhythm_score","memorability_score",
    "warmth_score","professionalism_score","overall_score",
    "territory","source_words",
   ],
  )
  self.assertEqual(len(exported),3)
