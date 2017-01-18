class ImageProcessor(object):
  """Prepares images for OCR processing

  Processing targets the specific problems: 
    - image rotation
    - image segmentation (find region of interest)
    - segmentation of roi by type (name fields, address fields, city, etc)
    - image clarity (OCR prep: black and white, noise reduction)

  """
  def __init__(self):
    pass

  def fix_image_skew(self):
    pass

  def find_region_of_interest(self):
    pass

  def segment_region_of_interest(self):
    pass
