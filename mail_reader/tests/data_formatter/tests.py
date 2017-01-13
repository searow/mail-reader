import unittest
import pandas as pd
import store_data_formatter as sdf

class TestDataFormatter(unittest.TestCase):
  def setUp(self):
    # TODO(searow): consider switching this to setUpClass for performance 

    # Load the desired data formatter object
    fname = './tests/data_formatter/BAP_example_data.xlsx'
    self.data_formatter = sdf.BAPDataFormatter(fname)

  def test_read_file_line_numbers(self):
    self.assertEqual(10, self.data_formatter.get_data_len())

  def test_read_first_line(self):
    ronald = self.data_formatter.data.iloc[0]
    self.assertEqual('MCDONALD, RONALD', ronald['NAME'])
    self.assertEqual(20, ronald['SUITE'])

  def test_import_all_data(self):
    data_lines = []

    while self.data_formatter.has_next_customer():
      line = self.data_formatter.format_next_customer()
      data_lines.append(line)

    # Test LOMBARDI, FALCO / 333 as last entry to import
    falco = data_lines[-1]
    self.assertEqual('LOMBARDI', falco[0][0])
    self.assertEqual('FALCO', falco[1][0])
    self.assertEqual(333, falco[0][1])
    self.assertEqual(333, falco[1][1])

  def tearDown(self):
    pass

if __name__ == '__main__':
  unittest.main()