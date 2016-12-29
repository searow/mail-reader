import unittest
import pandas as pd

class TestQuickNameAccessor(unittest.TestCase):
  def setUp(self):
    # TODO(searow): consider switching this to setUpClass for performance 
    fname = './tests/name_matching/name_to_box_number.xlsx'
    df = pd.read_excel(fname)
    headers = ['NAME', 'BOX']
    self.data = df[headers]

  def test_perfect_match_name_only_one_box(self):
    # NAILSALON, 101
    pass

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
