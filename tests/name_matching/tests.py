import unittest
import pandas as pd
import quick_name_accessor as qna
import store_data_formatter as sdf

class TestQuickNameAccessor(unittest.TestCase):
  def setUp(self):
    # TODO(searow): consider switching this to setUpClass for performance 
    fname = './tests/name_matching/name_to_box_number.xlsx'
    formatter = sdf.BAPDataFormatter(fname)
    self.name_accessor = qna.QuickNameAccess()
    self.name_accessor.create_entries_with_formatter(formatter)

  def test_add_name(self):
    pass

  def test_perfect_match_name_only_one_box(self):
    # NAILSALON, 101
    names = ['NAILSALON']
    boxes = self.name_accessor.find_matches_by_names(names)
    self.assertEqual(101, boxes[0])

  def test_perfect_match_name_multiple_boxes(self):
    # FOX MCCLOUD, 333/555
    # SLIPPY TOAD, 333/444
    pass

  def test_decent_match_only_one_box(self):
    # N4ILSALOON, 101
    pass

  def test_decent_match_multiple_boxes(self):
    # MARCUS MCOLOUD, 333/555
    pass

  def test_match_only_commons(self):
    # CLIFFORD THE BIG RED DOG INC, ???
    pass

  def test_no_remotely_close_match(self):
    # PEPPY HARE, ???
    pass

  def test_improperly_split_name(self):
    # FALCO LOM BARDI, 333
    pass

  def test_improperly_appended_names(self):
    # JAMESMCCLOUD, 555
    pass

  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()
