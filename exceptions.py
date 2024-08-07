class OpenStreamException(Exception):
  """Exception thrown if webcam cannot be opened"""

class WebcamReadException(Exception):
  """Exception thrown if frame cannot be read from webcam"""

class NoImageInDetectorException(Exception):
  """Exception thrown if AI Detector is called without an image being loaded"""