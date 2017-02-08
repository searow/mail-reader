import unittest
import mail_reader.vision.processing.image_process as image_processor
import mail_reader.vision.processing.ocr_processor as ocr_processor
import cv2

class TestImageProcessing(unittest.TestCase):
  # Tests preprocessing steps before OCR as well as OCR results. Many 
  # preprocessing functions are module level.
  def setUp(self):
    ocr = ocr_processor.TesseractProcessor()
    self.processor = image_processor.ImageProcessor(ocr)

    # Append each test image that we want to test here
    self.images = [] 
    self.images.append({
      'path' : './mail_reader/tests/vision/image_processing/test_image_0.jpg',
      'rotation_ans' : 0.97,
      'roi_ans' : (322, 690),
      'segmentation_quantity' : 4
      })
    self.images.append({
      'path' : './mail_reader/tests/vision/image_processing/test_image_1.jpg',
      'rotation_ans' : -6.46,
      'roi_ans' : (356, 565),
      'segmentation_quantity' : 6
      })

  def test_calculate_rotation(self):
    # Maximum +- error allowed in degrees
    error = 1

    for idx, data in enumerate(self.images):
      img = cv2.cvtColor(cv2.imread(data['path']), cv2.COLOR_RGB2GRAY)
      rotated_img, angle = image_processor._fix_image_rotation(
          img, self.processor.rotation_cfg)
      answer = data['rotation_ans']
      self.assertTrue(answer - error < angle < answer + error,
                      'Failed test ' + str(idx))

  def test_center_region_of_interest(self):
    # Note that when rotation is performed, the image is cropped on the edges
    # that do not fit, so the answer should reflect this. The image size 
    # doesn't ever change in rotation.

    # Success is based on point of center of area of interest. Must be within
    # +-5% of image width and height of real center.
    error = 0.05

    for idx, data in enumerate(self.images):
      img = cv2.cvtColor(cv2.imread(data['path']), cv2.COLOR_RGB2GRAY)
      # Rotate image
      rotated_img, angle = image_processor._fix_image_rotation(
          img, self.processor.rotation_cfg)

      # Image preprocessing
      _, thresh_img = cv2.threshold(rotated_img, thresh=0, maxval=255,
                                    type=cv2.THRESH_BINARY_INV + 
                                         cv2.THRESH_OTSU)

      # ROI detection
      contours = image_processor._identify_contours(
          img, self.processor.main_contour_cfg)
      img_center = (rotated_img.shape[0]/2, rotated_img.shape[1]/2)
      best_contour = image_processor._find_best_contour(contours, img_center)
      box, center = image_processor._get_box_from_contour(best_contour)

      # Check answer
      img_dims = img.shape
      error_range = (img_dims[0] * error, img_dims[1] * error)
      answer = data['roi_ans']
      self.assertTrue(answer[0] - error_range[0] < 
                      center[0] < 
                      answer[0] + error_range[0], 
                      'Failed test ' + str(idx))
      self.assertTrue(answer[1] - error_range[1] < 
                      center[1] < 
                      answer[1] + error_range[1], 
                      'Failed test ' + str(idx))

  def test_roi_segmentation_quantity(self):
    # Tests how many horizontal lines were read from the ROI in the image 
    for idx, data in enumerate(self.images):
      img = cv2.imread(data['path'])
      text = self.processor.get_text_lines(img)
      answer = data['segmentation_quantity']
      self.assertTrue(answer == len(text),
                      'Failed test ' + str(idx))

  def test_ocr_text_results(self):
    # TODO(searow): print actual test images on envelope and take pictures so
    #               don't have to use personal info. just print the text data
    #               for now as a placeholder
    for idx, data in enumerate(self.images):
      img = cv2.imread(data['path'])
      text = self.processor.get_text_lines(img)
      print(text)

  def tearDown(self):
    pass