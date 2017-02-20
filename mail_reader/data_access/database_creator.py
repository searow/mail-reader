import sqlite3
import pandas

class DatabaseCreator(object):
  """Creates an in-memory sqlite3 database using input data.

  Attributes:
    __db_conn: Sqlite database connection that will be eventually returned.
    __df: Pandas dataframe for file with data to put into database.
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
    self.__df = pandas.read_excel(path)
    # Create SQL database in memory and populate
    self.__db_conn = sqlite3.connect(':memory:')
    self.__create_tables()
    self.__populate_file_entries()

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

  def __populate_file_entries(self):
    pass


class BapDatabaseCreator(DatabaseCreator):
  """Subclass to handle specific data files."""
  def __init__(self):
    pass
