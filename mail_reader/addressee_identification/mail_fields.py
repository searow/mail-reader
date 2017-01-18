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
    pass