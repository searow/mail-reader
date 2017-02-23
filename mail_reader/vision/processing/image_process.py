import cv2
import numpy as np

def _fix_image_rotation(img, config):
  """Returns rotated image to horizontal and angle in degrees.

  Args:
    img: Image that contains rotation to be corrected.
    config: PreprocessConfig object containing rotation parameters.

  Returns:
    rotated_img: Image with rotation applied. Image is rotated about the 
                 centerpoint with edges cropped as needed.
    angle: Angle that the image was rotated. Positive angle means the image
           was rotated counter-clockwise to get to its new position.
  """
  contours = _identify_contours(img, config)

  # Throw exception if we can't find any contours
  if len(contours) == 0:
    raise NoContoursError

  # Use the largest contour to determine angle. Note that angle given is
  # -90 < angle <= 0, so correct sign to be how we want.
  rect = cv2.minAreaRect(contours[0])
  angle = rect[2]
  if angle < -45:
    angle += 90

  # Correct the image using center of image as rotation point. Anything that
  # falls outside the original image size due to rotation is cropped.
  rows, cols = img.shape
  M = cv2.getRotationMatrix2D((int(cols/2), int(rows/2)), angle, 1)
  rotated_img = cv2.warpAffine(img, M, (cols, rows))

  return rotated_img, angle

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

def _identify_contours(img, config):
  """Finds and returns contours in decreasing size order.

  Finds contours in 2 steps: 1) finds edges and removes noise 2) performs
  morphological closing operation to aggregate connected regions. The config
  provides the information on how to performs these options, specifically in
  the blur_kernel size (removes noise) and the morph_close_size which dictates
  how many pixels to include in the closing operation. Returns the associated
  contours in decreasing size order.

  Args:
    img: image to search
    config: PreprocessConfig object for configuration options

  Returns:
    Contours in decreasing order by pixel area
  """
  cleaned = _find_edges_and_remove_noise(img, config.blur_size)
  contours = _isolate_text_regions(cleaned, config.morph_close_size)

  return contours

def _crop_image_to_contour(img, contour):
  """Given an image and contour, crop the image to only include contour.

  Args:
    img: image to be cropped
    contour: contour on the image that designates the bounds to be cropped

  Returns:
    New cropped image only containing contour area
  """
  roi_box, center = _get_box_from_contour(contour)
  rows, cols = img.shape

  # Isolate ROI
  # Min values are 0 for bot/left, max are width or height for top/right
  # TODO(searow): Added a +-1 here to each to give a little more border. This
  #               probably isn't the best way to do this, but it's to make 
  #               sure that tesseract is outputting info.
  bot = min(roi_box[:,1] - 1)
  bot = 0 if bot < 0 else bot
  top = max(roi_box[:,1] + 1)
  top = rows if top >= rows else top
  left = min(roi_box[:,0] - 1)
  left = 0 if left < 0 else left
  right = max(roi_box[:,0] + 1)
  right = cols if right >= cols else right

  cropped_img = img[bot:top, left:right]

  return cropped_img

def _reorder_contours_by_position(contours):
  """Sorts contours by height position, closest to top = first.

  Args:
    contours: Contours to be sorted.

  Returns:
    Contours in sorted order by height position
  """
  # We sort here by the 2nd return value of _get_box_from_contour, which is
  # the height position of the center of the contour.
  in_order = sorted(contours, 
                    key=lambda item: _get_box_from_contour(item)[1][0])

  return in_order

def _remove_small_contours(contours):
  """Removes any contours that are too small to be valuable.

  Args:
    contours: List of contours to examine.

  Returns:
    Same list of contours, but with any tiny contours removed.
  """
  # We remove contours based on the height and width of the contour, found 
  # from max - min in each direction.
  # TODO(searow): currently setting to 15 pixels, should find the best value 
  #               to use here.
  min_px = 15
  remove_idx = []
  for idx, contour in enumerate(contours):
    heights = sorted(contour[:, :, 0])
    height = heights[-1] - heights[0]
    widths = sorted(contour[:, :, 1])
    width = widths[-1] - widths[0]

    if height < min_px or width < min_px:
      remove_idx.append(idx)

  # Filter out small contours 
  filtered = [c for idx, c in enumerate(contours) if idx not in remove_idx]
  return filtered


class PreprocessConfig(object):
  """Holds preprocessing configuration values for different operations."""

  def __init__(self, blur_size, morph_close_size):
    """Inits with desired sizes.

    Args:
      blur_size: tuple (x, y) of blur size for cleaning operations
      morph_close_size: tuple (x, y) of closing size for contour recognition
    """
    self.blur_size = blur_size
    self.morph_close_size = morph_close_size

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
    ocr_processor: OcrProcessor object responsible for actual OCR processing.
    original_image: Unaltered image to be processed.
    working_image: Working image workspace, constantly changing.
    preprocessed_images: Set of preprocessed images, ready for OCR.
  """
  # TODO(searow): these sizes are based on 720p camera set to 1280 x 720 
  #               resolution. they should probably be based on % of pixels
  #               since actual physical letter size dictates how many pixels
  #               to examine at a time.
  main_contour_cfg = PreprocessConfig((5, 5), (50, 50))
  # line_contour_cfg.morph_close_size currently being overriden in _preprocess
  line_contour_cfg = PreprocessConfig((5, 5), (50, 3))
  rotation_cfg = PreprocessConfig((5, 5), (40, 40))

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


    # Original image used for color reproduction and overlays if needed
    # working_image used for all forwards processes (things that won't need
    # to be reversed)
    self.original_image = image
    self.working_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Preprocess is ALL image manipulation before OCR, but not including OCR
    try:
      self._preprocess()
      ocr_results = self._perform_ocr()
    except NoContoursError:
      # Return an empty set if we don't have contours at any point in time.
      return []
    
    return ocr_results

  def _preprocess(self):
    """Preprocesses input image to prepare for OCR.

    Preprocessing handles all image manupulation. Returned image is ready for
    OCR analysis. Resulting images are instance variable preprocessed_images.

    Returns:
      None
    """
    # TODO(searow): refactor here to isolate each general step
    # Rotation correction
    rotated_img, angle = _fix_image_rotation(self.working_image, 
                                             self.rotation_cfg)
    # rotation = _calculate_rotation(self.working_image)
    # rotated_img = _rotate_image_ccwise(self.working_image, rotation)

    # Threshold to binary to allow morphological operations
    _, thresh_img = cv2.threshold(rotated_img, thresh=0, maxval=255,
                                  type=cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Identify the region of interest (ROI), which should be addressee label
    contours = _identify_contours(rotated_img, self.main_contour_cfg)
    img_center = (rotated_img.shape[0]/2, rotated_img.shape[1]/2)
    best_contour = _find_best_contour(contours, img_center)
    cropped_img = _crop_image_to_contour(rotated_img, best_contour)

    # Identify lines within ROI
    # TODO(searow): using width/2 for now, but consider putting this elsewhere
    self.line_contour_cfg.morph_close_size = (int(cropped_img.shape[1]/2), 2)
    contours = _identify_contours(cropped_img, self.line_contour_cfg)
    # Reorder contours in order of height position (top = first) and throw 
    # away anything small
    contours = _reorder_contours_by_position(contours)
    contours = _remove_small_contours(contours)

    # Threshold each image separately and add it to our pool to be OCR'd
    # TODO(searow): consider using only some of contours since we're currently
    #               using all of them
    img_set = []
    for contour in contours:
      line_img = _crop_image_to_contour(cropped_img, contour)
      _, thresh_img = cv2.threshold(
          line_img, thresh=0, maxval=255,
          type=cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
      img_set.append(thresh_img)

    self.preprocessed_images = img_set

  def _perform_ocr(self):
    """Performs OCR on image using ocr_processor.

    Returns:
      Array of strings representing individual lines on document
    """
    text_lines = []
    for im in self.preprocessed_images:
      text_lines.append(self.ocr_processor.get_text(im))

    return text_lines

class Error(Exception):
  pass

class NoContoursError(Error):
  """Occurs when contour finding functions can't find any useful contours."""
  pass
