import unittest
import mail_reader.addressee_identification.text_analyzer as text_analyzer

class TestTextAnalyzer(unittest.TestCase):
  def setUp(self):
    self.analyzer = text_analyzer.TextAnalyzer()

  def test_simple_address(self):
    lines = [
      'FOX MCCLOUD',
      '444 GREAT FOX CABIN DR',
      'CORNERIA, CA 90000'
    ]
    fields = self.analyzer.parse_text_lines(lines)
    self.assertTrue('FOX' in fields.addressee_line['all_names'])
    self.assertTrue('MCCLOUD' in fields.addressee_line['all_names'])
    self.assertTrue('444' in fields.street_line['number'])
    self.assertTrue('GREAT FOX CABIN' in fields.street_line['street_name'])
    self.assertTrue('CORNERIA' in fields.city_line['city'])
    self.assertTrue('CA' in fields.city_line['state'])
    self.assertTrue('90000' in fields.city_line['zip_code'])

  def test_actual_address(self):
    lines = [
      'DR ALBERT EINSTEIN',
      '112 MERCER STREET',
      'PRINCETON, NJ 08540'
    ]
    fields = self.analyzer.parse_text_lines(lines)
    self.assertTrue('DR' in fields.addressee_line['all_names'])
    self.assertTrue('ALBERT' in fields.addressee_line['all_names'])
    self.assertTrue('EINSTEIN' in fields.addressee_line['all_names'])
    self.assertTrue('112' in fields.street_line['number'])
    self.assertTrue('MERCER' in fields.street_line['street_name'])
    self.assertTrue('PRINCETON' in fields.city_line['city'])
    self.assertTrue('NJ' in fields.city_line['state'])
    self.assertTrue('08540' in fields.city_line['zip_code'])

  def test_variant_box_separate_line(self):
    box_names = ['PMB', 'BOX', '#', 'SUITE', 'PO BOX', 'POBOX', 'PO', '',
                 'PMB ', 'BOX ', '# ', 'SUITE ', 'PO BOX ', 'POBOX ', 'PO ']
    # Append box number to each of them separately
    for idx, name in enumerate(box_names):
      box_names[idx] = name + '102'

    lines = [
      'RONALD MCDONALD JR',
      '',
      '111 1/2 MEMORY LANE',
      'SAN FRANCISCO, CA 94101'
    ]

    # Test out each box name variant
    for name in box_names:
      test_lines = lines.copy()
      test_lines[1] += name
      fields = self.analyzer.parse_text_lines(test_lines)
      self.assertTrue('RONALD' in fields.addressee_line['all_names'])
      self.assertTrue('MCDONALD' in fields.addressee_line['all_names'])
      self.assertTrue('JR' in fields.addressee_line['all_names'])
      self.assertTrue('111' in fields.street_line['number'])
      self.assertTrue('MEMORY' in fields.street_line['street_name'])
      self.assertTrue('SAN FRANCISCO' in fields.city_line['city'])
      self.assertTrue('CA' in fields.city_line['state'])
      self.assertTrue('94101' in fields.city_line['zip_code'])
      self.assertTrue('102' in fields.probable_box,
                      'Failed box name type: ' + name)

  def test_variant_box_appended_to_street_line(self):
    box_names = ['PMB', 'BOX', '#', 'SUITE', 'PO BOX', 'POBOX', 'PO', '',
                 'PMB ', 'BOX ', '# ', 'SUITE ', 'PO BOX ', 'POBOX ', 'PO ']
    # Append box number to each of them separately
    for idx, name in enumerate(box_names):
      box_names[idx] = name + '102'

    lines = [
      'RONALD MCDONALD JR',
      '111 1/2 MEMORY LANE ',
      'SAN FRANCISCO, CA 94101'
    ]

    # Test out each box name variant
    for name in box_names:
      # Append the box name to the 2nd line
      test_lines = lines.copy()
      test_lines[1] += name
      fields = self.analyzer.parse_text_lines(test_lines)
      self.assertTrue('RONALD' in fields.addressee_line['all_names'])
      self.assertTrue('MCDONALD' in fields.addressee_line['all_names'])
      self.assertTrue('JR' in fields.addressee_line['all_names'])
      self.assertTrue('111' in fields.street_line['number'])
      self.assertTrue('MEMORY' in fields.street_line['street_name'])
      self.assertTrue('SAN FRANCISCO' in fields.city_line['city'])
      self.assertTrue('CA' in fields.city_line['state'])
      self.assertTrue('94101' in fields.city_line['zip_code'])
      self.assertTrue('102' in fields.probable_box,
                      'Failed box name type: ' + name)

  def test_variant_box_separate_line_and_appended_suite(self):
    box_names = ['PMB', 'BOX', '#', 'SUITE', 'PO BOX', 'POBOX', 'PO', '',
                 'PMB ', 'BOX ', '# ', 'SUITE ', 'PO BOX ', 'POBOX ', 'PO ']
    # Append box number to each of them separately
    for idx, name in enumerate(box_names):
      box_names[idx] = name + '102'

    lines = [
      'RONALD MCDONALD JR',
      '',
      '111 1/2 MEMORY LANE SUITE 7A',
      'SAN FRANCISCO, CA 94101'
    ]

    # Test out each box name variant
    for name in box_names:
      # Use test_lines instead to create a fresh version of lines to do the 
      # appending for the tests
      test_lines = lines.copy()
      test_lines[1] += name
      fields = self.analyzer.parse_text_lines(test_lines)
      self.assertTrue('RONALD' in fields.addressee_line['all_names'])
      self.assertTrue('MCDONALD' in fields.addressee_line['all_names'])
      self.assertTrue('JR' in fields.addressee_line['all_names'])
      self.assertTrue('111' in fields.street_line['number'])
      self.assertTrue('MEMORY' in fields.street_line['street_name'])
      self.assertTrue('SAN FRANCISCO' in fields.city_line['city'])
      self.assertTrue('CA' in fields.city_line['state'])
      self.assertTrue('94101' in fields.city_line['zip_code'])
      self.assertTrue('102' in fields.probable_box,
                      'Failed box name type: ' + name)

  def test_garbage_in_first_lines(self):
    lines = [
      '@||| 1 ((@',
      'SFHHHHEJ 1231CCC IIII111029',
      '',
      'OSCAR THE GROUCH',
      'TRASH CAN',
      '123 SESAME STREET',
      'MANHATTAN, NEW YORK 10010'
    ]

    fields = self.analyzer.parse_text_lines(lines)
    self.assertTrue('OSCAR' in fields.addressee_line['all_names'])
    self.assertTrue('THE' in fields.addressee_line['all_names'])
    self.assertTrue('GROUCH' in fields.addressee_line['all_names'])
    self.assertTrue('TRASH' in fields.addressee_line['all_names'])
    self.assertTrue('CAN' in fields.addressee_line['all_names'])
    self.assertTrue('123' in fields.street_line['number'])
    self.assertTrue('SESAME' in fields.street_line['street_name'])
    self.assertTrue('MANHATTAN' in fields.city_line['city'])
    self.assertTrue('NEW YORK' in fields.city_line['state'])
    self.assertTrue('10010' in fields.city_line['zip_code'])

  def test_garbage_in_middle_lines(self):
    lines = [
      'MR ALOYSIUS SNUFFLEUPAGUS',
      '|||! !((@     ',
      '',
      '123 SESAME STREET',
      'MANHATTAN, NEW YORK 10010'
    ]
    fields = self.analyzer.parse_text_lines(lines)
    self.assertTrue('MR' in fields.addressee_line['all_names'])
    self.assertTrue('ALOYSIUS' in fields.addressee_line['all_names'])
    self.assertTrue('SNUFFLEUPAGUS' in fields.addressee_line['all_names'])
    self.assertTrue('123' in fields.street_line['number'])
    self.assertTrue('SESAME' in fields.street_line['street_name'])
    self.assertTrue('MANHATTAN' in fields.city_line['city'])
    self.assertTrue('NEW YORK' in fields.city_line['state'])
    self.assertTrue('10010' in fields.city_line['zip_code'])


  def tearDown(self):
    pass
