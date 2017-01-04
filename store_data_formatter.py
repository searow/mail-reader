import abc
import pandas as pd
import re

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
    self.data_len = super().get_data_len()
    self.current_import_idx = 0

  def format_next_customer(self):
    '''Returns formatted customer names and box numbers

    Reads the next customer from the data. Splits up the line items into 
    standard data format that all StoreDataFormatters will use. Returns this 
    standard data format for use by the actual in-memory storage object.

    Returns:
      Nested list of names and suites: [['NAME0', SUITE#],['NAME1', SUITE#],...]
    '''

    line = self.data.iloc[self.current_import_idx]
    self.current_import_idx += 1

    # Name splitting occurs here
    customers = []
    name = line['NAME']
    suite = line['SUITE']
    clean_name = self._remove_redundant_identifiers(name)
    name_split = self._split_name_remove_empty(clean_name)
    for item in name_split:
      customers.append([item, suite])

    return customers 

  def _split_name_remove_empty(self, name):
    delimiters = r'[, ]'
    name = name.replace('.','')
    name_split = list(filter(None, re.split(delimiters, name)))

    return name_split

  def _remove_redundant_identifiers(self, name):
    '''Removes less useful words, such as INC, MR, MRS, JR, CO'''
    # TODO(searow): need to implement this
    return name

  def has_next_customer(self):
    '''Checks if there are more customers to format'''
    return self.current_import_idx < self.data_len
