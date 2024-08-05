from cv2 import FONT_HERSHEY_DUPLEX,FONT_HERSHEY_PLAIN, LINE_AA, rectangle, putText,getTextSize
import numpy as np

class Visualiser:
  def __init__(self):
    self.fps_avg_frame_count = 8

  def show_fps(self, frame, fps, webcam):
    # Show the FPS
    row_size = 50  # pixels
    left_margin = 24  # pixels
    colour = (0, 0, 0)  # black
    size = 1
    thickness = 1
    fps_text = f'FPS = {fps:.1f}'
    text_location = (left_margin, row_size)
    webcam.overlay_text(frame, fps_text, text_location, FONT_HERSHEY_DUPLEX, size, colour, thickness, LINE_AA)

  def draw_text(self,frame, text,
          font=FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          font_scale=3,
          font_thickness=2,
          text_color=(0, 255, 0),
          text_color_bg=(0, 0, 0)
          ):

    x, y = pos
    text_size, _ = getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    rectangle(frame, pos, (x + text_w+2, y + text_h+2), text_color_bg, -1)
    putText(frame, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)
    return text_size

  def upadte_frame(self,frame,detection_result) -> np.ndarray:
    MARGIN = 10  # pixels
    ROW_SIZE = 30  # pixels
    FONT_SIZE = 1
    FONT_THICKNESS = 1
    TEXT_COLOR = (0, 0, 0)  # black
    FONT_STYLE = FONT_HERSHEY_PLAIN
    for detection in detection_result.detections:
      # Draw bounding_box
      bbox = detection.bounding_box
      start_point = bbox.origin_x, bbox.origin_y
      end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
      # Use the orange color for high visibility.
      rectangle(frame, start_point, end_point, (0, 255, 255), 2)

      # Draw label and score
      category = detection.categories[0]
      category_name = category.category_name
      probability = round(category.score, 2)
      result_text = category_name + ' (' + str(probability) + ')'
      text_location = (bbox.origin_x,
                      bbox.origin_y-10)
      self.draw_text(frame, result_text, FONT_STYLE, text_location, font_scale=FONT_SIZE, font_thickness=FONT_THICKNESS, text_color=TEXT_COLOR, text_color_bg=(0,255,255))
    return frame