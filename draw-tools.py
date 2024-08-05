import cv2

class Draw_tools:
  def __init__(self, frame):
    self.frame = frame

  def overlay_text(self, frame, text, location, font, size, colour, thickness, line_style):
    return cv2.putText(
                frame, text, location, font, size, colour, thickness, 
                line_style, size, colour, thickness, line_style)  