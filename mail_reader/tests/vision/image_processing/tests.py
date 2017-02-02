import unittest
import mail_reader.vision.processing.image_process as image_processor
import mail_reader.vision.processing.ocr_processor as ocr_processor
import cv2

class TestImageProcessing(unittest.TestCase):
  def setUp(self):
    ocr = ocr_processor.TesseractProcessor()
    self.processor = image_processor.ImageProcessor(ocr)

    # Append each test image that we want to test here
    self.images = [] 
    self.images.append({
      'path' : './mail_reader/tests/vision/image_processing/test_image_0.jpg',
      'rotation_ans' : 0.97,
      'roi_ans' : (695, 324)
      })
    self.images.append({
      'path' : './mail_reader/tests/vision/image_processing/test_image_1.jpg',
      'rotation_ans' : -6.46,
      'roi_ans' : (600, 429)
      })

  def test_calculate_rotation(self):
    # Maximum +- error allowed in degrees
    error = 1

    for data in self.images:
      img = cv2.cvtColor(cv2.imread(data['path']), cv2.COLOR_RGB2GRAY)
      self.processor.original_image = img
      rotation = self.processor._calculate_rotation()
      answer = data['rotation_ans']
      self.assertTrue(answer - error < rotation < answer + error)

  def test_center_region_of_interest(self):
    # Success is based on point of center of area of interest. Must be within
    # +-5% of image width and height of real center.
    pass

  def test_roi_segmentation_quantity(self):
    pass

  def test_ocr_text_results(self):
    pass

  def tearDown(self):
    pass