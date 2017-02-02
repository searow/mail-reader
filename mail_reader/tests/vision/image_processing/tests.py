import unittest
import mail_reader.vision.processing.image_process as image_processor
import mail_reader.vision.processing.ocr_processor as ocr_processor
import cv2

class TestImageProcessing(unittest.TestCase):
  def setUp(self):
    ocr = ocr_processor.TesseractProcessor()
    self.processor = image_processor.ImageProcessor(ocr)
    pass

  def test_calculate_rotation(self):
    # Maximum +- error allowed in degrees
    error = 1

    # Append each image that we want to test here
    images = []  # [filepath, answer]
    images.append(['./mail_reader/tests/vision/image_processing/test_image_0_97.jpg', 0.97])
    images.append(['./mail_reader/tests/vision/image_processing/test_image_6_46.jpg', -6.46])

    for [path, ans] in images:
      img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_RGB2GRAY)
      self.processor.original_image = img
      rotation = self.processor._calculate_rotation()
      self.assertTrue(ans - error < rotation < ans + error)

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