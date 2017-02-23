import unittest
import sqlite3
import re
import pandas
import mail_reader.data_access.box_matching as box_matching
import mail_reader.data_access.database_creator as database_creator
import mail_reader.addressee_identification.mail_fields as mail_fields

class TestQuickNameAccessor(unittest.TestCase):
  @classmethod
  def setUpClass(self):
    # Database creation is expensive, so we're setting up here. If making any
    # database changes, make sure to use a separate instance!
    self.path = './20161209.xlsx'
    # Create database from customer data file
    creator = database_creator.BapDatabaseCreator()
    self.conn = creator.create_database_from_excel(self.path)

  def setUp(self):
    pass

  def test_simple_box_score_evaluation(self):
    # Simple test to make sure _get_box_scores is working properly
    name = 'MCCLOUD'
    match_list = [
        ['MCCLOUD', 333], 
        ['MCCLOUD', 555],
        ['MCCLOUD', 555],
        ['MCDONALD', 20]
    ]
    box_multiplier = [0, 10, 555]
    # We don't normally cane about flaot truncation, but these decimals are set
    # based on what we'd normally get out of the function.
    answer = {
        333: 1.0,
        555: 2.0,
        20: 0.5333333333333333
    }

    result = box_matching._get_box_scores(name, match_list, box_multiplier)
    self.assertEqual(answer, result)

  def test_combine_box_scores(self):
    # Tests to make sure we're returning the proper scores in the right order
    scores_1 = {
        111: 1.7,
        20: 0.7,
        4: 0.2,
        390: 0.9
    }
    scores_2 = {
        111: 1.6,
        3: 0.2,
        390: 1.0,
        52: 0.8
    }
    scores_3 = {
        909: 0.5,
        3: 1.0
    }
    answer = [
        [111, 3.3],
        [390, 1.9],
        [3, 1.2],
        [52, 0.8],
        [20, 0.7],
        [909, 0.5],
        [4, 0.2]
    ]
    
    result = box_matching._combine_boxes_scores([scores_1, scores_2, scores_3])
    self.assertEqual(answer, result)

  def test_all_entries_including_suites(self):
    # The input of this test is the raw data from the database. It uses the
    # suite number as well as the input names that are greater than 2 
    # letters long.

    # Create the box matcher and set the database connection
    matcher = box_matching.BoxMatcher()
    matcher.set_database_connection(self.conn)
    # Set our answer database information 
    df = pandas.read_excel(self.path)

    # For each row, populate a MailFields object with known info and test that 
    # the output is correct
    errors = []
    for idx, row in enumerate(df.iterrows()):
      key = row[1]
      # Only test active lines
      if not key['Active']:
        continue
      names = database_creator._split_names(key['NAME'])
      # Only test names that are more than 1 letter long.
      names = [i for i in names if len(i) > 1]
      if not names:
        continue

      # Set fresh MailFields object for each of the data points
      input_fields = mail_fields.MailFields()
      input_fields.addressee_line['all_names'] = names
      input_fields.probable_box = [key['SUITE']]
      matches = matcher.get_matches(input_fields)

      # Checks are here instead of asserts. Append to error list as needed.
      if not matches[0]['box_number'] == key['SUITE']:
        errors.append({
          'raw_name': key['NAME'],
          'solved_suite': matches[0]['box_number'],
          'correct_suite': key['SUITE'],
          'matches': matches
        })
      if idx % 500 == 0:
        print('Completed idx = ' + str(idx))
    for error in errors:
      print('Raw name: ' + str(error['raw_name']))
      print('Solved suite: ' + str(error['solved_suite']))
      print('Correct suite: ' + str(error['correct_suite']))
      print('First 5 matches:')
      for idx, match in enumerate(error['matches']):
        if idx < 5:
          print('  Box: ' + str(match['box_number']) + 
                ' Score: ' + str(match['score']))
    self.assertEqual(len(errors), 0)

  def test_all_entries_without_suites(self):
    # The input of this test is the raw data from the database. It omits the
    # suite number and uses the input names that are greater than 2 
    # letters long.

    # Create the box matcher and set the database connection
    matcher = box_matching.BoxMatcher()
    matcher.set_database_connection(self.conn)
    # Set our answer database information 
    df = pandas.read_excel(self.path)

    # For each row, populate a MailFields object with known info and test that 
    # the output is correct
    errors = []
    for idx, row in enumerate(df.iterrows()):
      key = row[1]
      # Only test active lines
      if not key['Active']:
        continue
      names = database_creator._split_names(key['NAME'])
      # Only test names that are more than 1 letter long.
      names = [i for i in names if len(i) > 1]
      if not names:
        continue

      # Set fresh MailFields object for each of the data points
      input_fields = mail_fields.MailFields()
      input_fields.addressee_line['all_names'] = names
      matches = matcher.get_matches(input_fields)

      # Checks are here instead of asserts. Append to error list as needed.
      if not matches[0]['box_number'] == key['SUITE']:
        errors.append({
          'raw_name': key['NAME'],
          'solved_suite': matches[0]['box_number'],
          'correct_suite': key['SUITE'],
          'matches': matches
        })
      if idx % 500 == 0:
        print('Completed idx = ' + str(idx))
    for error in errors:
      print('Raw name: ' + str(error['raw_name']))
      print('Solved suite: ' + str(error['solved_suite']))
      print('Correct suite: ' + str(error['correct_suite']))
      print('First 5 matches:')
      for idx, match in enumerate(error['matches']):
        if idx < 5:
          print('  Box: ' + str(match['box_number']) + 
                ' Score: ' + str(match['score']))
    self.assertEqual(len(errors), 0)

  def test_single_custom_name(self):
    # Create the box matcher and set the database connection
    matcher = box_matching.BoxMatcher()
    matcher.set_database_connection(self.conn)

    input_fields = mail_fields.MailFields()
    input_fields.addressee_line['all_names'] = ['TEST','NAME']
    matches = matcher.get_matches(input_fields)
    print(matches[0])

  def tearDown(self):
    pass

  @classmethod
  def tearDownClass(self):
    pass

if __name__ == '__main__':
  unittest.main()
