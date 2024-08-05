from ai_analyser import Ai_analyser
from webcam import Webcam
from ffmpeg import Ffmpeg
from visualiser import Visualiser
from os import environ
from time import time
from Exceptions import OpenStreamException,WebcamReadException,NoImageInDetectorException

class Application:
  def __init__(self, cam_uri, model, score_threshold, frame_width, frame_height, rtmp_out, max_results):
    self.cam_uri = cam_uri
    self.model = model
    self.score_threshold = score_threshold
    self.width = frame_width
    self.height = frame_height
    self.rtmp_out = rtmp_out
    try:
      self.webcam = Webcam(self.cam_uri, self.width, self.height)
    except OpenStreamException as e:
      return None
    self.ffmpeg = Ffmpeg(self.rtmp_out)
    self.ai_analyser = Ai_analyser(model, score_threshold, max_results)
    self.visualiser = Visualiser()

  def run(self):
    while self.webcam.is_open():
      start_time = time()
      try:
        frame = self.webcam.read_frame()
        frame = self.webcam.convert_to_rgb(frame)
        self.ai_analyser.add_image(frame)
        self.ai_analyser.detect()
        self.visualiser.show_fps()
        result_frame = self.ai_analyser.render_result()
      except WebcamReadException as wre:
        print(f'Error: {wre}')
        continue
      except NoImageInDetectorException as nid:
        print(f'Error {nid}')
        continue
      

if __name__ == '__main__':
  cam_uri = environ.get('CAM_URI')
  rtmp_out = environ.get('RTMP_OUT')
  score_threshold = environ.get('SCORE_THRESHOLD')
  model = environ.get('MODEL')
  app = Application(cam_uri, model, score_threshold, 640, 360, rtmp_out, 5)
  if (app is not None):
    app.run()