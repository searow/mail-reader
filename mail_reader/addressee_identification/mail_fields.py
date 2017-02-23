class MailFields(object):
  """Represents fields detected in addressee section of mail

  Addressee section is comprised of lines of notification (names, 
  type of entity being addressed, reason for address) and physical identifiers
  (physical address, box/suite #s, city, state, zip). MailFields is reponsible
  for accepting different types of identifiers and providing a common object to
  pass between processing objects that represents potential identifiers in the
  addressee section. TextAnalyzer is responsible for populating these fields.
  """

  def __init__(self):
    self.addressee_line = {
        'all_names': [],  # All names as list
    }
    self.probable_box = []  # Store as string in case there's something weird
    self.street_line = {
        'number': [],  # Store as string in case there's something weird
        'street_name': [],
    }
    self.city_line = {
        'city': [],
        'state': [],
        'zip_code': []  # 5 digit zip only
    }

  def is_populated(self):
    """Returns true if MailFields has enough fields to be useful."""
    # Only condition right now is that there are names in the all_names field.
    # This check is mostly to make sure other parts of the name matching
    # don't fail.
    if len(self.addressee_line['all_names']) > 0:
      return True

    return False
