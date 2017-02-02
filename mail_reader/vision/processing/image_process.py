import cv2

class ImageProcessor(object):
  """Prepares images for OCR processing.

  Processing targets the specific problems: 
    - image rotation
    - image segmentation (find region of interest)
    - segmentation of roi by type (name fields, address fields, city, etc)
    - image clarity (OCR prep: black and white, noise reduction)

  Ultimately is responsible for creating strings of text that represent what
  is on the mail itself.

  Attributes:
    ocr_processor: OcrProcessor object responsible for actual OCR processing
    original_image: unaltered image to be processed
    working_image: working image workspace, constantly changing
  """
  def __init__(self, ocr_processor):
    """Inits with an OcrProcessor to specify OCR engine"""
    self.ocr_processor = ocr_processor

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
    from horizontal, clockwise. The amount of counterclockwise rotation to 
    correct the image to be horizontal is the negative of the return value.

    Returns:
      Angle of rotation in degrees.
    """

    blur_kernel = (5, 5)
    # (40, 40) closing kernel seems pretty good for 720p image for addressee
    close_struct = (40, 40)

    img = self._find_edges_and_remove_noise(self.original_image, blur_kernel)
    contours = self._isolate_text_regions(img, close_struct)

    rect = cv2.minAreaRect(contours[0])
    angle = rect[2]
    if angle < -45:
      angle += 90

    return angle

  def _find_edges_and_remove_noise(self, img, blur_size):
    '''Returns an image with noise removed

    Accepts a grayscale image, identifies regions of interest, and removes any
    noise in the image.

    Args:
      img: image to process in grayscale
      blur_size: tuple containing (width, height) parameters for blur size

    Returns:
      image containing regions of interest with noise removed
    '''

    # Find the edges in the image, using 1st order sobel operator in both
    # directions 
    img = cv2.Sobel(img, ddepth=-1, dx=1, dy=1)

    # Remove noise from image
    img = cv2.blur(img, ksize=blur_size)
    _, img = cv2.threshold(img, thresh=0, maxval=255,
                           type=cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return img

  def _isolate_text_regions(self, img, closing_size):
    '''Returns a list of contours that contain potential text regions

    Uses a thresholded image with edges defined to find text regions. Input image
    needs to have text edges highligted. Performs closing operation to create
    filled contours to find regions of text

    Args:
      img: thresholded image to find text regions
      closing_size: tuple containing (width, height) of closing element

    Returns:
      List of contours in sorted order by contour area
    '''

    # Morph closing to fill in the text areas. Use a large rectangle b/c we want
    # text regions to be physically connected
    close_elem = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=closing_size)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, close_elem)

    # Find and sort the contours by area
    _, cont, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(cont, key=cv2.contourArea, reverse=True)

    return contours

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
