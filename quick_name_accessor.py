import store_data_formatter as sdf

class QuickNameAccess(object):
  '''Allows quick name lookups to get related box numbers

  Names are accessed via dictionary that has its keys set as the first letter
  in the word. This splits the lookup space by ~26, but must have first letter
  of name from OCR be correct.

  Attributes:
    letter_access: dictionary of letters containing names starting with
                   that letter
  '''

  def __init__(self):
    '''Init with empty access dictionary'''
    self.letter_access = {}

  def create_entries_with_formatter(self, data_formatter):
    while data_formatter.has_next_customer():
      line = data_formatter.format_next_customer()

      # Each line can have multiple customers, so process each individually
      for item in line:
        name = item[0]
        box = item[1]
        letter = name[0]
        entry = QuickAccessEntry(name, box)
        self.add_entry(letter, entry)

  def find_matches_by_name(self, name):
    '''Given a set of names to identify boxholder, returns best box matches

    Name matching is performed by edit distance. Matches do not have to be 
    perfect to work.

    Args:
      name: list of strings of name to identify boxholder

    Returns:
      List of box numbers as strings, in descending order of match strength
    '''
    pass

  def add_entry(self, letter, entry):
    '''Adds entry to the access object

    Args:
      letter: letter to add the to entry
      entry: QuickAccessEntry object to add 
    '''

    # TODO(searow): add checks for letters being only 1 letter

    # We need to create the letter dict entry if it doesn't exist
    if not letter in self.letter_access.keys():
      self.letter_access[letter] = []

    self.letter_access[letter].append(entry)

class QuickAccessEntry(object):
  '''Entries for the QuickNameAccess object'''

  def __init__(self, name, box_num):
    '''Inits entry with a name associated with a box number

    Args:
      name: string name to be added
      box_num: box number that the name is registered to

    Returns:
      None
    '''

    self.name = name
    self.box_num = box_num
