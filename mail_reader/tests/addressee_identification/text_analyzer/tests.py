import unittest
import mail_reader.addressee_identification.text_analyzer as text_analyzer

class TestTextAnalyzer(unittest.TestCase):
  def setUp(self):
    self.analyzer = text_analyzer.TextAnalyzer()

  def test_simple_address(self):
    lines = [
      ['FOX MCCLOUD'],
      ['444 GREAT FOX CABIN DR'],
      ['CORNERIA, CA 90000']
    ]
    fields = self.analyzer.parse_text_lines(lines)
    self.assertEqual(fields.addressee_line['first_name'], 'FOX')
    self.assertEqual(fields.addressee_line['last_name'], 'MCCLOUD')
    self.assertEqual(fields.street_line['number'], "444")
    self.assertEqual(fields.street_line['street_name'], 'GREAT FOX CABIN DR')
    self.assertEqual(fields.city_line['city'], 'CORNERIA')
    self.assertEqual(fields.city_line['state'], 'CA')
    self.assertEqual(fields.city_line['zip_code'], 90000)
    
  def test_actual_address(self):
    lines = [
      ['DR ALBERT EINSTEIN'],
      ['112 MERCER STREET'],
      ['PRINCETON, NJ 08540']
    ]
    fields = self.analyzer.parse_text_lines(lines)
    self.assertEqual(fields.addressee_line['prefix'], 'DR')
    self.assertEqual(fields.addressee_line['first_name'], 'ALBERT')
    self.assertEqual(fields.addressee_line['last_name'], 'EINSTEIN')
    self.assertEqual(fields.street_line['number'], 112)
    self.assertEqual(fields.street_line['street_name'], 'MERCER STREET')
    self.assertEqual(fields.city_line['city'], 'PRINCETON')
    self.assertEqual(fields.city_line['state'], 'NJ')
    self.assertEqual(fields.city_line['zip_code'], 8540)

  def test_variant_box_separate_line(self):
    box_names = ['PMB', 'BOX', '#', 'SUITE', 'PO BOX', 'POBOX', 'PO', '',
                 'PMB ', 'BOX ', '# ', 'SUITE ', 'PO BOX ', 'POBOX ', 'PO ']
    # Append box number to each of them separately
    for idx, name in enumerate(box_names):
      box_names[idx] = name + '102'

    lines = [
      ['RONALD MCDONALD JR'],
      [''],
      ['111 1/2 MEMORY LANE'],
      ['SAN FRANCISCO, CA 94101']
    ]
    fields = self.analyzer.parse_text_lines(lines)

    # Test out each box name variant
    for name in box_names:
      lines[1] = name
      self.assertEqual(fields.addressee_line['first_name'], 'RONALD')
      self.assertEqual(fields.addressee_line['last_name'], 'MCDONALD')
      self.assertEqual(fields.addressee_line['suffix'], 'JR')
      self.assertEqual(fields.street_line['number'], "111 1/2")
      self.assertEqual(fields.street_line['street_name'], 'MEMORY LANE')
      self.assertEqual(fields.city_line['city'], 'SAN FRANCISCO')
      self.assertEqual(fields.city_line['state'], 'CA')
      self.assertEqual(fields.city_line['zip_code'], 94101)
      self.assertEqual(fields.probable_box, '102',
                       'Failed box name type: ' + name)

  def test_variant_box_appended_to_street_line(self):
    box_names = ['PMB', 'BOX', '#', 'SUITE', 'PO BOX', 'POBOX', 'PO', '',
                 'PMB ', 'BOX ', '# ', 'SUITE ', 'PO BOX ', 'POBOX ', 'PO ']
    # Append box number to each of them separately
    for idx, name in enumerate(box_names):
      box_names[idx] = name + '102'

    lines = [
      ['RONALD MCDONALD JR'],
      ['111 1/2 MEMORY LANE '],
      ['SAN FRANCISCO, CA 94101']
    ]
    fields = self.analyzer.parse_text_lines(lines)

    # Test out each box name variant
    for name in box_names:
      # Append the box name to the 2nd line
      lines[1] = name + lines[1][0]
      self.assertEqual(fields.addressee_line['first_name'], 'RONALD')
      self.assertEqual(fields.addressee_line['last_name'], 'MCDONALD')
      self.assertEqual(fields.addressee_line['suffix'], 'JR')
      self.assertEqual(fields.street_line['number'], "111 1/2")
      self.assertEqual(fields.street_line['street_name'], 'MEMORY LANE')
      self.assertEqual(fields.city_line['city'], 'SAN FRANCISCO')
      self.assertEqual(fields.city_line['state'], 'CA')
      self.assertEqual(fields.city_line['zip_code'], 94101)
      self.assertEqual(fields.probable_box, '102',
                       'Failed box name type: ' + name)

  def tearDown(self):
    pass
