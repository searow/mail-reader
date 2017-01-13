import unittest
import pandas as pd
import mail_reader.data_access.quick_name_accessor as qna
import mail_reader.data_access.store_data_formatter as sdf

class TestQuickNameAccessor(unittest.TestCase):
  def setUp(self):
    # TODO(searow): consider switching this to setUpClass for performance 
    fname = './mail_reader/tests/name_matching/name_to_box_number.xlsx'
    formatter = sdf.BAPDataFormatter(fname)
    self.name_accessor = qna.QuickNameAccess()
    self.name_accessor.create_entries_with_formatter(formatter)

  def test_add_name(self):
    pass

  def test_perfect_match_name_only_one_box(self):
    # NAILSALON, 101
    names = ['NAILSALON']
    boxes = self.name_accessor.find_matches_by_names(names)
    self.assertEqual(101, boxes[0][0])

  def test_perfect_match_name_multiple_boxes(self):
    # FOX MCCLOUD, 333/555
    # SLIPPY TOAD, 333/444
    names = ['FOX', 'MCCLOUD']
    boxes = self.name_accessor.find_matches_by_names(names)
    boxes = boxes[0:2]
    self.assertTrue(any(333 in item for item in boxes)) 
    self.assertTrue(any(555 in item for item in boxes)) 

    names = ['SLIPPY', 'TOAD']
    boxes = self.name_accessor.find_matches_by_names(names)
    boxes = boxes[0:2]
    self.assertTrue(any(333 in item for item in boxes)) 
    self.assertTrue(any(444 in item for item in boxes)) 

  def test_decent_match_only_one_box(self):
    # N4ILSALOON, 101
    names = ['N4ILSALOON']
    boxes = self.name_accessor.find_matches_by_names(names)
    self.assertEqual(101, boxes[0][0])

  def test_decent_match_multiple_boxes(self):
    # MARCUS MCOLOUD, 333/555
    names = ['MARCUS', 'MCOLOUD']
    boxes = self.name_accessor.find_matches_by_names(names)
    self.assertTrue(any(333 in item for item in boxes))
    self.assertTrue(any(555 in item for item in boxes))

  def test_match_only_commons(self):
    # CLIFFORD THE BIG RED DOG INC, ???
    # TODO(searow): need to add bad matches handling and no matching letter
    #               exception handling for this one
    pass

  def test_no_remotely_close_match(self):
    # PEPPY HARE, ???
    # TODO(searow): need to add bad matches handling and no matching letter
    #               exception handling for this one
    pass

  def test_improperly_split_name(self):
    # FALCO LOM BARDI, 333
    names = ['FALCO', 'LOM', 'BARDI']
    boxes = self.name_accessor.find_matches_by_names(names)
    self.assertEqual(333, boxes[0][0])

  def test_improperly_appended_names(self):
    # JAMESMCCLOUD, 555
    names = ['JAMESMCCLOUD']
    boxes = self.name_accessor.find_matches_by_names(names)
    self.assertEqual(555, boxes[0][0])

  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
