class MailFields(object):
  """Represents fields detected in addressee section of mail

  Addressee section is comprised of lines of notification (names, 
  type of entity being addressed, reason for address) and physical identifiers
  (physical address, box/suite #s, city, state, zip). MailFields is reponsible
  for accepting different types of identifiers and providing a common object to
  pass between processing objects that represents potential identifiers in the
  addressee section. TextAnalyzer is responsible for populating these fields.
  """
  self.addressee_line = {
      'prefix': None,  # Mr. Mrs. Dr.
      'first_name': None,
      'last_name': None,
      'suffix': None,  # Jr. Sr. III Esq
      'all_names': None,  # All names as list
      'secondary_entity': None  # Alternate person or name
  }
  self.probable_box = None
  self.street_line = {
      'number': None,
      'street_name': None,
      'secondary_id': None,  # APT, SUITE, ETC
  }
  self.city_line = {
      'city': None,
      'state': None,
      'zip_code': None  # 5 digit zip only
  }

  def __init__(self):
    pass
