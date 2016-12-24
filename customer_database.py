class CustomerDatabase(object):
  '''Customer database access class

  CustomerDatabase provides a means to load, save, and access customer 
  information. There are two primary functions: 1) Given a name string, find
  boxes that most closely match the string 2) Given a box number, return the
  customers that are registered to that box

  '''

  def __init__(self):
    pass

  def load_existing_database(self, fname):
    '''Loads pre-existing database into memory

    Args:
      fname: name of json file containing database

    Returns:
      None
    '''
    pass

  def find_matching_boxes(self, name):
    '''Returns boxes with potential matches to input string

    Given a name, find the boxes that best match that name. Will only include
    boxes that pass a given threshold of confidence.

    Args:
      name: name to use to identify the box holder

    Returns:
      List of strings identifying potential box matches
    '''
    pass

  def get_active_boxholders(self, box_num):
    '''Returns list of active names in box

    Given a box number, returns a list of active names registered to the box. 
    Returned names are same as the default name string obtained from the 
    original customer database file.

    Args:
      box_num: box number to read

    Returns:
      List of names for active box holders in box
    '''
    pass