import abc

class OcrProcessor(metaclass=abc.ABCMeta):
  """Generic OCR processing object."""
  def __init__(self):
    pass

  @abc.abstractmethod
  def get_text(self, image):
    """Performs OCR on desired image, returns result string"""
    pass

class TesseractProcessor(OcrProcessor):
  """OCR processing using Tesseract.

  This will likely be the default OCR processing object, but others can be 
  used if desired.
  """
  def __init__(self):
    super().__init__()

  def get_text(self, image):
    """Performs OCR on image, returns result string"""
    pass