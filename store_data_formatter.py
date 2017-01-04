import abc
import pandas as pd

class StoreDataFormatter(metaclass=abc.ABCMeta):
  '''Abstract class to format existing customer data 

  This class should be subclassed based on a store's custom data storage
  format. Greenville Shipping Center should subclass this class into
  GreenvilleDataFormatter, which allows Greenville's customer data to be 
  formatted into a way that private_mailbox.py and quick_name_accessor.py can
  use the information.
  '''

  def __init__(self, fname):
    pass

  @abc.abstractmethod
  def format_next_customer(self):
    '''Returns formatted version of next customer line-item, if it exists'''
    pass

  def get_data_len(self):
    '''Returns number of line items stored'''
    return len(self.data)

class BAPDataFormatter(StoreDataFormatter):
  '''DataFormatter subclass for BAP store'''

  def __init__(self, fname):
    '''Read the data file and store it in memory

    Args:
      fname: excel file name containing the data to be formatted

    Returns:
      None
    '''
    df = pd.read_excel(fname)
    headers = ['NAME', 'SUITE']
    self.data = df[headers]

  def format_next_customer(self):
    pass
