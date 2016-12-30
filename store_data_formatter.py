import abc

class StoreDataFormatter(metaclass=abc.ABCMeta):
  '''Abstract class to format existing customer data 

  This class should be subclassed based on a store's custom data storage
  format. Greenville Shipping Center should subclass this class into
  GreenvilleDataFormatter, which allows Greenville's customer data to be 
  formatted into a way that private_mailbox.py and quick_name_accessor.py can
  use the information.
  '''

  def __init__(self):
    '''Read the data file and store it in memory'''
    pass

  @abc.abstractmethod
  def format_next_customer(self):
    '''Returns formatted version of next customer line-item, if it exists'''
    pass
