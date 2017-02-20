import unittest
import mail_reader.data_access.database_creator as database_creator

class TestDatabaseCreator(unittest.TestCase):
  def setUp(self):
    pass

  def test_create_database_from_excel_file(self):
    path = './mail_reader/tests/data_access/sample_data.xlsx'
    creator = database_creator.DatabaseCreator()
    db = creator.create_database_from_excel(path)
    c = db.cursor()
    c.execute('SELECT * FROM box_entities;')
    result = c.fetchall()
    answer = [(111, 0), (5, 1), (22, 2), (111, 3)]
    self.assertEqual(result, answer)

  def tearDown(self):
    pass
