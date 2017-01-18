class ImageProcessor(object):
  """Prepares images for OCR processing.

  Processing targets the specific problems: 
    - image rotation
    - image segmentation (find region of interest)
    - segmentation of roi by type (name fields, address fields, city, etc)
    - image clarity (OCR prep: black and white, noise reduction)

  """
  def __init__(self):
    pass

  def set_base_image(self, image):
    """Sets base image - original image to analyze.

    Creates working image reference also, which will be used to perform 
    sequential image processing steps so we can refer to original image if 
    needed.

    Args:
      image: image to analyze

    Returns:
      None
    """
    pass

  def get_mail_fields(self):
    """Returns MailFields that contains addressee information obtained from OCR.

    Returns:
      MailFields object with addressee information.
    """
    pass

  def fix_image_skew(self):
    """Calculates image skew and rotates image to be horizontal.

    Returns:
      None
    """
    pass

  def find_region_of_interest(self):
    """Finds best match for region of interest.
    
    Region of interest for letter mail is addressee section.

    Returns:
      Points of smallest bounding box encompassing region of interest
    """
    pass

  def segment_region_of_interest(self):
    """Crops region of interest and segments image.

    Segmentation of region of interest is meant to find addressee lines as 
    well as words within each addressee line.

    Returns:
      Nested list of horizontal addressee lines and individual words within
      each line. [[line_1_word_1, line_1_word_2],[line_2_word_1,
      line_2_word_2, line_2_word_3], etc]
    """
    pass
