import mail_reader.addressee_identification.mail_fields as mail_fields
import usaddress
import re
import string

def _alnum_percent(line):
  """Calculates % of alphanumeric characters in string.

  Args:
    line: String to calculate

  Returns:
    Percentage of alphanumeric characters, as a decimal (90% alnum = 0.9)
  """
  total = len(line)

  test_set = set()
  for letter in string.ascii_letters:
    test_set.add(letter)
  test_set.add(' ')

  # Return a failure (no good characters) if there are no characters
  if total < 1:
    return 0

  alnum_count = 0
  star_count = 0
  bar_count = 0
  for letter in line:
    # if letter.isalnum():
    if letter in test_set:
      alnum_count += 1
    if letter == '*':
      star_count += 1
    if letter == 'I' or letter == 'i' or letter == 'l' or letter == '|':
      bar_count += 1

  # TODO(searow): properly implement this, but sticking this here for now.

  if star_count / total > 0.1:
    return 0

  if bar_count / total > 0.5:
    return 0

  return alnum_count / total

class TextAnalyzer(object):
  """Analyzes text segments for addressee identifiers. 

  Allows communication to other objects by populating a MailFields object. 
  """

  def __init__(self):
    pass

  def parse_text_lines(self, text_lines):
    """Analyzes text lines, in order read from OCR processing.

    Populates the MailFields object with information gathered from OCR. Uses
    information from each of the lines to best figure out who is the main
    addresssee and which box it is trying to reach.
  
    Args:
      text_lines: nested list of text lines read from OCR
                  [[line_1_word_1, line_1_word_2], [line_2_word_1,
                   line_2_word_2, line_2_word_3]]
    Returns:
      None
    """

    self.__fields = mail_fields.MailFields()

    alphanum_threshold = 0.5

    # Only evaluate lines that are predominantly alphanumeric
    for line in text_lines:
      if _alnum_percent(line) > alphanum_threshold:  
        try:
          parsed = usaddress.tag(line)[0]
        except usaddress.RepeatedLabelError as e:
          # If usaddress gets confused, just throw away the answer as if
          # we got nothing for now.
          # TODO(searow): fix this to handle multiple tags and labels.
          parsed = {}
        for tag in parsed:
          self._add_to_fields(tag, parsed[tag])
    return self.__fields

  def _add_to_fields(self, tag, data):
    """Adds the parsed items to the MailFields object.

    Args:
      tag: Key from usaddress.parse() result.
      data: Data corresponding to tag from usaddress.parse() result.

    Returns:
      None.
    """
    # Addressee data
    if 'Recipient' == tag:
      names = data.split()
      for name in names:
        self.__fields.addressee_line['all_names'].append(name) 

    # Probable box data
    # Strip out anything that's not a number since we might get some other
    # data inside here also. If the box # can be a subnumber (BOX 102-A) then
    # we'll end up putting everything in the # only.
    if 'USPSBoxGroupID' == tag or 'USPSBoxGroupType' == tag or \
        'USPSBoxID' == tag or 'USPSBoxType' == tag or \
        'OccupancyType' == tag or 'OccupancyIdentifier' == tag or \
        'SubaddressType' == tag or 'SubaddressIdentifier' == tag:
      box = re.search('\d+', data)
      if box is not None:
        self.__fields.probable_box.append(box.group(0)) 

    # Street data
    # Discarding street number prefix and suffix for now
    if 'AddressNumber' == tag:
      self.__fields.street_line['number'].append(data) 
    if 'StreetName' == tag:
      self.__fields.street_line['street_name'].append(data) 

    # City data
    if 'PlaceName' == tag:
      self.__fields.city_line['city'].append(data) 
    if 'StateName' == tag:
      self.__fields.city_line['state'].append(data) 
    if 'ZipCode' == tag:
      self.__fields.city_line['zip_code'].append(data) 
