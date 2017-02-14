import mail_reader.addressee_identification.text_analyzer
import mail_reader.vision.processing.image_process

class AddresseeReader(object):
  """Manages image processing and text analysis reader.

  Attributes:
    img_processor: ImageProcessor object responsible for OCR.
    text_analyzer: TextAnalyzer object responsible for analyzing addressee
                   strings and populating MailFields object
  """
  def __init__(self, processor, analyzer):
    self.__img_processor = processor
    self.__text_analyzer = analyzer

  def get_mail_fields(self, image):
    """Analyzes image and populates associated MailFields object.

    Args:
      image: Image to be analyzed.

    Returns:
      MailFields object with addressee information populated.
    """
    lines = self.__img_processor.get_text_lines(image)
    fields = self.__text_analyzer.parse_text_lines(lines)
    
    return fields
