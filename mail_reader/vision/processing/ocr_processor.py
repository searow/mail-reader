import abc
import pyocr
from PIL import Image

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
    tools = pyocr.get_available_tools()
    # TODO(searow): do proper error handling if ocr tools not installed
    self.tool = tools[0]

  def get_text(self, image):
    """Performs OCR on image, returns result string"""
    txt = self.tool.image_to_string(Image.fromarray(image),
                                    builder=pyocr.builders.TextBuilder())
    
    return txt
