import unittest

class TestImageProcessing(unittest.TestCase):
  def setUp(self):
    pass

  def test_image_process_rotate_horizontal(self):
    # Cannot be more than +-5% different from real rotation angle value
    pass

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