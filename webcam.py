import cv2

from exceptions import OpenStreamException,WebcamReadException


class Webcam:
  def __init__(self, cam_uri, width, height):
    self.cam_uri = cam_uri
    self.width = width
    self.height = height
    self.frame = None
    try:
      self.webcam_feed = cv2.VideoCapture(self.cam_uri)
      self.webcam_feed.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
      self.webcam_feed.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
    except Exception as e:
      raise OpenStreamException(f"Cannot open webcam stream: {e.toString()}")

  def is_open(self):
    return self.webcam_feed.isOpened()
  
  def read_frame(self):
    success, frame = self.webcam_feed.read()
    if not success:
      raise WebcamReadException("Unable to read frame from webcam")
    self.frame = frame
    return frame
  
  def get_current_frame(self):
    return self.frame
  
  def convert_to_rgb(self, frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
  def overlay_text(self, frame, text, location, font, size, colour, thickness, line_style):
    return cv2.putText(
                frame, text, location, font, size, colour, thickness, 
                line_style, size, colour, thickness, line_style)
    
  def break_key(self):
    return cv2.waitKey(1)