import unittest
import pandas

class TestDatabaseCreator(unittest.TestCase):
  def setUp(self):
    pass

  def test_create_database_from_excel_file(self):
    path = './mail_reader/tests/data_access/sample_data.xlsx'
    creator = DatabaseCreator()
    db = creator.create_database(path)

  def tearDown(self):
    pass
