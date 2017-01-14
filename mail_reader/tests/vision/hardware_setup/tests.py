import unittest
import mail_reader.vision.hardware.access_webcam as webcam

class TestLogitechC270Webcam(unittest.TestCase):
  def setUp(self):
    # USB webcam is 1 here b/c laptop has 1 integrated webcam already. Choose
    # the correct webcam number to get the C270
    webcam_id = 1

    self.cam = webcam.LogitechC270()
    self.cam.open_webcam_id(webcam_id) 

  def test_proper_resolution(self):
    res = self.cam.get_resolution()
    self.assertEqual((1280, 720), res)

  def test_capture_frame(self):
    # TODO(searow): add exception cases, particularly webcam not found and
    #               webcam in use. others?
    image = self.cam.get_frame()
    self.assertIsNotNone(image)

  def tearDown(self):
    self.cam.close_camera()
