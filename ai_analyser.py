from mediapipe.tasks.python import vision
import mediapipe as mp
from mediapipe.tasks import python
from time import time,time_ns
from exceptions import NoImageInDetectorException
from visualiser import Visualiser

class Ai_analyser:
  def __init__(self, model, score_threshold, max_results):
    self.model = model
    self.score_threshold = score_threshold
    self.max_results = max_results
    self.detection_frame = None
    self.detection_result_list = []
    self.fps_avg_frame_count = 8
    self.start_time = time()
    self.counter = 0
    self.fps = 0
    self.base_options = python.BaseOptions(model_asset_path=self.model)
    self.current_image = None
    options = vision.ObjectDetectorOptions(
                    base_options=self.base_options,
                    running_mode=vision.RunningMode.LIVE_STREAM,
                    max_results=self.max_results, 
                    score_threshold=self.score_threshold,
                    result_callback=self.save_result)
    self.detector = vision.ObjectDetector.create_from_options(options)
    
  def save_result(self, result: vision.ObjectDetectorResult, unused_output_image: mp.Image, timestamp_ms: int):

      # Calculate the FPS
      if self.counter % self.fps_avg_frame_count == 0:
          self.fps = self.fps_avg_frame_count / (time() - self.start_time)
          self.start_time = time()

      self.detection_result_list.append(result)
      self.counter += 1
  
  def get_fps(self):
    return self.fps
  
  def add_image(self, frame):
    self.current_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)


  def detect(self):
    if (self.current_image is not None):
      self.detector.detect_async(self.current_image, time_ns() // 1_000_000)
    else:
      raise NoImageInDetectorException(f'No image has been loaded in the detector')
    
  def render_result(self, visualiser, orig_image):
    image = orig_image
    if self.detection_result_list:
      image = visualiser.update_frame(orig_image, self.detection_result_list[0])
      self.detection_result_list.clear()
    return image

  def terminate(self):
    self.detector.close()