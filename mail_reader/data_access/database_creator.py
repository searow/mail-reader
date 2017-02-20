import sqlite3
import pandas
import re

def _split_names(raw_name):
  """Splits name string into list of strings based on delimiter.

  Removes periods (doesn't replace with space), then removes based on 
  delimiter. Delimiter set to be spaces and commas, specifically to split based
  on most common delimiters in customer database.

  Args:
    raw_name: String of name to be split 'THE BE.AR COMPANY, LLC'.

  Returns:
    List of strings split into parts : ['THE', 'BEAR', 'COMPANY', 'LLC'].
  """
  # Remove periods from raw name, no replacement
  names = raw_name.replace('.','')
  # Split name by commas and spaces
  names = filter(None, re.split(r'[, ]', names))

  return names

class DatabaseCreator(object):
  """Creates an in-memory sqlite3 database using input data.

  Attributes:
    __db_conn: Sqlite database connection that will be eventually returned.
    _df: Pandas dataframe for file with data to put into database.
  """
  def __init__(self):
    pass

  def create_database_from_excel(self, path):
    """Creates database from excel file.

    Args:
      path: File path pointing to .xlsx file to read.

    Returns:
      In-memory sqlite database.
    """
    # Save excel data into memory
    self._df = pandas.read_excel(path)
    self._column_reformat()
    # Create SQL database in memory and populate
    self.__db_conn = sqlite3.connect(':memory:')
    self.__create_tables()
    self.__populate_file_entries()

    return self.__db_conn

  def _column_reformat(self):
    """Method to override so dataframe instance variable can be modified.

    Method is called after pandas.read_excel() is called so we can perform
    maintenance on the dataframe in case the column headers need modification.
    Base class is not implemented since it uses the default column names.
    """
    pass

  def __create_tables(self):
    """Manually create tables to populate."""
    # TODO(searow): should probably change this later to parameterize, but 
    #               this will do for now.
    c = self.__db_conn.cursor()
    # TODO(searow): no idea if this is the right way to define the schema.
    #               take a look at this again after learning more.
    c.execute("""
        CREATE TABLE box_activities (
            box_id  INTEGER,
            active  BOOLEAN,
            PRIMARY KEY (box_id)
        );
    """)
    c.execute("""
        CREATE TABLE entity_statuses (
            entity_id  INTEGER,
            current    BOOLEAN,
            PRIMARY KEY (entity_id)
        );
    """)
    c.execute("""
        CREATE TABLE unique_entity_names (
            entity_id           INTEGER,
            unique_entity_name  TEXT,
            PRIMARY KEY (entity_id, unique_entity_name),
            FOREIGN KEY (entity_id)
                REFERENCES entity_statuses(entity_id)
        );
    """)
    c.execute("""
        CREATE TABLE box_entities (
            box_id     INTEGER,
            entity_id  INTEGER,
            PRIMARY KEY (box_id, entity_id),
            FOREIGN KEY (box_id)
                REFERENCES box_activities(box_id),
            FOREIGN KEY (entity_id)
                REFERENCES entity_statuses(entity_id)
        );
    """)

    self.__db_conn.commit()

  def __populate_file_entries(self):
    """Populates database with data in excel file."""
    c = self.__db_conn.cursor()
    active_boxes = self.__determine_active_boxes()

    # Populate box_activities table first since that data is aggregate
    for box in active_boxes:
      c.execute('''
          INSERT INTO box_activities (box_id, active)
          VALUES (?, ?)
      ''', (box, active_boxes[box]))

    # Populate the rest of the tables since we have the active_boxes data, 
    # going row by row and adding items.
    for idx, row in enumerate(self._df.iterrows()):
      key = row[1]
      # Table entity_statuses
      c.execute('''
          INSERT INTO entity_statuses (entity_id, current)
          VALUES (?, ?);
      ''', (idx, key['ACTIVE']))

      # Table unique_entity_names
      # Catch IntegrityError here since we might be adding non-unique 
      # combinations of entity_id + unique_entity_name. We don't need to do
      # anything to handle them for now.
      raw_name = key['NAME']
      names = _split_names(raw_name)
      # Insert every name into the database, skipping integrity errors
      for name in names:
        try:
          c.execute('''
              INSERT INTO unique_entity_names (entity_id, unique_entity_name)
              VALUES (?, ?);
          ''', (idx, name))
        except sqlite3.IntegrityError:
          pass

      # Table box_entities
      c.execute('''
          INSERT INTO box_entities (box_id, entity_id)
          VALUES (?, ?);
      ''', (key['SUITE'], idx))

    self.__db_conn.commit()

  def __determine_active_boxes(self):
    """Checks dataframe to determine if boxes are active."""
    # Check all of the boxes. Set default box status to inactive and look for
    # any active ones. Result stored in boxes dictionary and returned.
    boxes = {}
    for row in self._df.iterrows():
      keys = row[1]
      # Set defaults to inactive
      if keys['SUITE'] not in boxes:
        boxes[keys['SUITE']] = False
      boxes[keys['SUITE']] |= keys['ACTIVE']

    return boxes

class BapDatabaseCreator(DatabaseCreator):
  """Subclass to handle specific data files."""
  def __init__(self):
    pass

  def _column_reformat(self):
    super()._column_reformat()
    # Standard format is all caps. Our data isn't all caps, so translate it.
    self._df.rename(columns=lambda x: x.upper(), inplace=True)
