class BoxMatcher(object):
  """Performs box matching operations to match MailFields with box number.

  Given a MailFields object and a database to access, finds the best matches
  to the database.

  Attributes:
    __database: Database from which to get box data.
  """
  def __init__(self):
    pass

  def get_matches(self, mail_fields):
    """Returns best matches of MailFields to database.

    Args:
      mail_fields: MailFields object to match database data to.

    Returns:
      List of box numbers with associated match score:
        [[box, score], [box, score], ...]
    """
    pass

  def set_database(self, database):
    """Sets database to use for box matching.

    Args:
      database: Database to access.

    Returns:
      None.
    """
    pass
