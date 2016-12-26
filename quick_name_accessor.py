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

  def find_matches_by_name(self, name):
    '''Given a name to identify the boxholder, returns best box matches

    Args:
      name: string of name to identify boxholder

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
