import cv2

class CustomWebcam(object):
  """Interface for interacting with webcam to obtain live images"""

  def __init__(self):
    pass

  def open_webcam_id(self, id):
    """Opens desired webcam hardware by webcam id

    Args:
      id: int of id representing hardware webcam number to open

    Returns:
      None
    """
  
    # TODO(searow): add exception here for other video captures and lack of 
    #               webcams. 
    self.cap = cv2.VideoCapture(id)

  def get_frame(self):
    """Grabs single frame from webcam

    Returns:
      Single frame as image
    """
    ret, frame = self.cap.read()

    return frame

  def close_camera(self):
    """Performs closing operations, call after done with all camera ops"""
    self.cap.release()

  def get_resolution(self):
    """Returns camera resolution setting as (width_px, height_px)"""
    width_px = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height_px = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    return (width_px, height_px)

class LogitechC270(CustomWebcam):
  """Logitech C270 webcam

  Attributes:
    resolution: tuple of (width pixels, height pixels)
  """

  resolution = (1280, 720)

  def open_webcam_id(self, id):
    """Opens webcam and also sets resolution for Logitech model C270"""
    super().open_webcam_id(id)
    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
