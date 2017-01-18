class TextAnalyzer(object):
  """Analyzes text segments for addressee identifiers. 

  Allows communication to other objects by populating a MailFields object. 
  """

  def __init__(self, mail_fields):
    """Inits with a MailFields object to populate"""
    pass

  def parse_text_lines(self, text_lines):
    """Analyzes text lines, in order read from OCR processing.

    Populates the MailFields object with information gathered from OCR. Uses
    information from each of the lines to best figure out who is the main
    addresssee and which box it is trying to reach.

    Args:
      text_lines: nested list of text lines read from OCR
                  [[line_1_word_1, line_1_word_2], [line_2_word_1,
                   line_2_word_2, line_2_word_3]]
    Returns:
      None
    """
    pass
