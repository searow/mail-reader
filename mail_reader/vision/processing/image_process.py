class ImageProcessor(object):
  """Prepares images for OCR processing.

  Processing targets the specific problems: 
    - image rotation
    - image segmentation (find region of interest)
    - segmentation of roi by type (name fields, address fields, city, etc)
    - image clarity (OCR prep: black and white, noise reduction)

  Ultimately is responsible for creating strings of text that represent what
  is on the mail itself.
  """
  def __init__(self, ocr_processor):
    """Inits with an OcrProcessor to specify OCR engine"""
    pass

  def get_text_lines(self, image):
    """Finds and returns addressee text lines.
    
    Performs image preprocessing steps, uses OcrProcessor to perform OCR on the 
    preprocessed image, and returns the text lines that are in the addressee 
    section of the image.

    Args:
      image: Image of the mail item that is to be processed.

    Returns:
      Array of strings representing each line that was read.
    """
    pass

  def _process_image(self):
    """Sets base image - original image to analyze.

    Creates working image reference also, which will be used to perform 
    sequential image processing steps so we can refer to original image if 
    needed.

    Returns:
      None
    """
    pass

  def _get_mail_fields(self):
    """Returns MailFields that contains addressee information obtained from OCR.

    Returns:
      MailFields object with addressee information.
    """
    pass

  def _calculate_rotation(self):
    """Calculates rotation angle of the image from horizontal, in degrees

    Rotation angle is given in degrees, representing the current rotation value
    from horizontal, counterclockwise. The amount of clockwise rotation to 
    correct the image to be horizontal is the negative of the return value.

    Returns:
      Angle of rotation in degrees.
    """
    pass


  def _rotate_image(self, angle):
    """Rotates image by angle.

    Rotated image keeps the entire original field of view visible. The 
    resulting image is larger than the original due to extra white space from
    rotation.

    Returns:
      None
    """
    pass

  def _find_region_of_interest(self):
    """Finds best match for region of interest.
    
    Region of interest for letter mail is addressee section.

    Returns:
      Points of smallest bounding box encompassing region of interest
    """
    pass

  def _segment_region_of_interest(self):
    """Crops region of interest and segments image.

    Segmentation of region of interest is meant to find addressee lines as 
    well as words within each addressee line.

    Returns:
      Nested list of horizontal addressee lines and individual words within
      each line. [[line_1_word_1, line_1_word_2],[line_2_word_1,
      line_2_word_2, line_2_word_3], etc]
    """
    pass
