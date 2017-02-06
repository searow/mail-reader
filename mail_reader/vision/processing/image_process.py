import cv2
import numpy as np

def _calculate_rotation(image):
  """Calculates rotation angle of the image from horizontal, in degrees

  Rotation angle is given in degrees, representing the current rotation value
  from horizontal, clockwise. 

  Returns:
    Angle of rotation in degrees.
  """

  blur_kernel = (5, 5)
  # (40, 40) closing kernel seems pretty good for 720p image for addressee
  close_struct = (40, 40)

  cleaned = _find_edges_and_remove_noise(image, blur_kernel)
  contours = _isolate_text_regions(cleaned, close_struct)

  rect = cv2.minAreaRect(contours[0])
  angle = rect[2]
  if angle < -45:
    angle += 90

  return angle
  
def _rotate_image_ccwise(image, angle):
  """Rotates image by angle.

  Rotated image keeps the entire original field of view visible. The 
  resulting image is larger than the original due to extra white space from
  rotation.

  Args:
    image: Image to be rotated
    angle: Angle to rotate image. Positive = counterclockwise rotation

  Returns:
    None
  """
  rows, cols = image.shape

  # Rotate image around center point of original image, cropping anything 
  # that falls outside of original range. 
  M = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)), angle, 1)
  rotated = cv2.warpAffine(image, M, (cols, rows))

  return rotated

def _find_edges_and_remove_noise(img, blur_size):
  """Returns an image with noise removed.

  Accepts a grayscale image, identifies regions of interest, and removes any
  noise in the image.

  Args:
    img: image to process in grayscale
    blur_size: tuple containing (width, height) parameters for blur size

  Returns:
    image containing regions of interest with noise removed
  """

  # Find the edges in the image, using 1st order sobel operator in both
  # directions 
  edges = cv2.Sobel(img, ddepth=-1, dx=1, dy=1)

  # Remove noise from image
  blurred = cv2.blur(edges, ksize=blur_size)
  _, cleaned = cv2.threshold(blurred, thresh=0, maxval=255,
                             type=cv2.THRESH_BINARY + cv2.THRESH_OTSU)

  return cleaned

def _find_best_contour(contours, center):
  """Finds best contour, weighted by contour area and distance from center.
  
  Region of interest for letter mail is addressee section. For manual mail
  scanning, region of interest will be heavily biased by position. Center of
  the image is set for heavy weighting of ROI.

  Returns:
    Points of smallest bounding box encompassing region of interest
  """

  # rows, cols = image.shape
  # center = [int(rows/2), int(cols/2)]
  # Maximum distance is from center (0,0) to any corner (+-rows/2,+-cols/2)
  max_dist = np.sqrt((center[1])**2 + (center[0])**2)

  # Only use the 5 largest contours. If any more, our image probably
  # has too much going on in it
  max_contours = 5
  max_contour_area = cv2.contourArea(contours[0])

  # Calculate and add the score values for each contour
  scores = []
  for c in contours[:5]:

    moments = cv2.moments(c)

    if moments['m00'] == 0:
      moments['m00'] = 1
    cent_row = int(moments['m10']/moments['m00'])
    cent_col = int(moments['m01']/moments['m00'])
    dist = np.sqrt((cent_row - center[0])**2 + 
                   (cent_col - center[1])**2)

    norm_dist = 1 - dist/max_dist
    norm_area = cv2.contourArea(c)/max_contour_area

    score = norm_dist * norm_area
    scores.append(score)

  # We only use the largest value, which will normally be idx 0
  max_score_idx = np.argmax(scores)

  return contours[max_score_idx]

def _get_box_from_contour(contour):
  """Returns the minimum box containing the contour (4 corner pts)

  Args:
    contour: contour object from _find_best_contour method, represents the
             outline contour detected

  Returns:
    Four corner points of minimum containing rectangle (box) and the coords
    of (height, width) of center
  """
  rect = cv2.minAreaRect(contour)
  box = np.int0(cv2.boxPoints(rect))

  center_height = np.mean(box[:, 1])
  center_width = np.mean(box[:, 0])

  return box, (center_height, center_width)

def _isolate_text_regions(img, closing_size):
  """Returns a list of contours that contain potential text regions

  Uses a thresholded image with edges defined to find text regions. Input image
  needs to have text edges highligted. Performs closing operation to create
  filled contours to find regions of text

  Args:
    img: thresholded image to find text regions
    closing_size: tuple containing (width, height) of closing element

  Returns:
    List of contours in sorted order by contour area
  """

  # Morph closing to fill in the text areas. Use a large rectangle b/c we want
  # text regions to be physically connected
  close_elem = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=closing_size)
  closed_img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, close_elem)

  # Find and sort the contours by area
  # TODO(searow): maybe don't need closed_img.copy() since we're creating 
  #               a new copy in closed_img anyways and not modifying img?
  _, cont, _ = cv2.findContours(closed_img.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
  contours = sorted(cont, key=cv2.contourArea, reverse=True)

  return contours

def _get_text_line_contours(img):
  """Finds horizontal lines of text and returns the contours.

  Horizontal lines of text are found via morphological closing operation. The
  best matches are used to determine the region of interest.

  Returns:
    List of contours in descending area order
  """

  blur_size = (5, 5)
  text_find_size = (50, 50)
  cleaned = _find_edges_and_remove_noise(img, blur_size)
  contours = _isolate_text_regions(cleaned, text_find_size)

  return contours  

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

    # - Save image and working copy (grayscale first)
    # - Preprocess image
    #   Rotation
    #   - Find rotation
    #   - Perform rotation
    #   Image handling
    #   - Threshold
    #   Image identification
    #   - _get_text_line_contours
    #   - _find_best_contour
    #   - _get_box_from_contour
    #   Prepare ROI for OCR
    #   - segment image (subsection image using ROI)
    #   - clean image (opening operation?)
    #   - copy image for analysis
    #   - text line contours again, but thin horizontals

    # Original image used for color reproduction and overlays if needed
    # working_image used for all forwards processes (things that won't need
    # to be reversed)
    self.original_image = image
    self.working_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    preprocessed_image = self._preprocess()

    ocr_results = self._perform_ocr()

    return ocr_results

  def _process_image(self):
    """Sets base image - original image to analyze.

    Creates working image reference also, which will be used to perform 
    sequential image processing steps so we can refer to original image if 
    needed.

    Returns:
      None
    """
    pass

  def _perform_ocr(self):
    """Performs OCR on image using ocr_processor.

    Returns:
      Array of strings representing individual lines on document
    """
    pass

  def _get_mail_fields(self):
    """Returns MailFields that contains addressee information obtained from OCR.

    Returns:
      MailFields object with addressee information.
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
