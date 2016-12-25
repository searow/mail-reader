class MailboxStore(object):
  '''Represents mailbox store, which is a group of mailboxes

  Attributes:
    boxes: dictionary of boxes, with string keys for box numbers
  '''

  def __init__(self):
    '''Init with empty dict for storing box keys'''
    self.boxes = {}

  def add_box(self, box_num, box):
    '''Adds single box to mailbox store

    Args:
      box_num: physical box number
      box: box representing physical mailbox in the store

    Returns:
      None
    '''

    box_num = str(box_num)

    # Make sure the box we're adding is empty
    if box_num in self.boxes.keys():
      raise BoxError('Box ' + box_num + ' already exists', box_num)

    self.boxes[box_num] = box

  def get_box(self, box_num):
    '''Returns the mailbox object registered to the box number

    Args:
      box_num: physical box number as string

    Returns:
      PrivateMailbox object representing the physical mailbox
    '''

    box_num = str(box_num)

    # Make sure the box we're adding exists
    if not box_num in self.boxes.keys():
      raise BoxError('Box ' + box_num + ' doesn\'t exist', box_num)

    return self.boxes[box_num]


class PrivateMailbox(object):
  '''Represents a physical mailbox

  PrivateMailbox represents the physical mailbox in the private mailbox store.
  It consists of BoxHolder objects.

  Attributes:
    boxholders: list of boxholder objects that are registered to that box
  '''

  def __init__(self):
    self.boxholders = []

  def add_boxholder(self, boxholder):
    '''Adds boxholder to this box

    Args:
      boxholder: can be a person or company box holder

    Returns:
      None
    '''
    self.boxholders.append(boxholder)

  def get_active_names(self):
    '''Returns only the active names in the box

    Returns:
      List of active, default names registered to the box
    '''

    active_names = []

    for bh in boxholders:
      if bh.is_active:
        active_names.append(bh.default_name)

    return active_names

  def get_all_names(self):
    '''Returns all of the names registered to the box

    Returns:
      List of all default names registered to the box
    '''
    pass

class BoxHolder(object):
  '''A BoxHolder is a single entity tied to a box number.

  BoxHolder represents a name tied to a box. Boxes contain BoxHolders. 
  BoxHolders can be people, business names, aliases, pretty much anything
  that can be used to reference an entity to whom something is being mailed.
  Each box often contains multiple BoxHolders.

  Attributes:
    default_name: default string saved in database
    is_active: bool for active boxholder. Could be inactive from non payments
               or from no longer customer (closed box)
  '''
  def __init__(self, default_name, is_active):
    self.default_name = name
    self.is_active = is_active

class PersonBoxHolder(BoxHolder):
  '''Represents a BoxHolder that is a single human entity
  
  Attributes:
    last_name: string of customer's last name
    other_names: list of strings containing other names, typically consisting
                 of first name and middle names/initials
  '''
  def __init__(self, default_name, is_active):
    '''Creates a BoxHolder that represents a person

    Uses the last entry in default_name as the last name of the person and
    the remaining names (in order) as the other_names list

    Args:
      default_name: default string saved in database
      is_active: bool for whether or not the BoxHolder is an active paying
                 customer 
    '''
    super(default_name, is_active)
    self.last_name = default_name[-1]
    self.other_names = default_name[0:-1]

class CompanyBoxHolder(BoxHolder):
  '''Represents a BoxHolder that is a not a human

  CompanyBoxHolder will typically be a company or alternate alias that has no
  natural ordering of names. IE: Morgans Box Alterations. Company name may 
  contain other natural identifiers, such as LLC, Corp, etc.

  Attributes:
    names: list of strings containing all the names in default order, ie: 
           ['Morgans', 'Box', 'Alterations']
  '''
  def __init__(self, default_name, is_active):
    '''Creates a BoxHolder that is represents a company/non-person alias

    Args:
      default_name: default string saved in database
      is_active: bool for whether or not the BoxHolder is an active paying
                 customer 
    '''
    super(default_name, is_active)
    self.names = default_name.split


class Error(Exception):
  pass

class BoxError(Error):
  '''Occurs when trying to perform operations accessing Boxes'''
  def __init__(self, message, box_num):
    self.message = message
    self.box_num = box_num
