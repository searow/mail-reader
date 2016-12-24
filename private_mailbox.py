class PrivateMailbox(object):
  '''Represents a physical mailbox

  PrivateMailbox represents the physical mailbox in the private mailbox store.
  It consists of BoxHolder objects.

  Attributes:
    boxholders: list of boxholder objects that are registered to that box
  '''

  def __init__(self):
    pass

  def add_boxholder(self, boxholder):
    '''Adds boxholder to this box

    Args:
      boxholder: can be a person or company box holder

    Returns:
      None
    '''
    pass

  def get_active_names(self):
    '''Returns only the active names in the box

    Returns:
      List of active, default names registered to the box
    '''
    pass

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
    super(default_name is_active)
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

