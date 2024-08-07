from ai_analyser import Ai_analyser
from webcam import Webcam
from ffmpeg import Ffmpeg
from visualiser import Visualiser
from os import environ
from time import time,sleep
from exceptions import OpenStreamException,WebcamReadException,NoImageInDetectorException

class Application:
  def __init__(self, cam_uri, model, score_threshold, frame_width, frame_height, rtmp_out, max_results):
    self.cam_uri = cam_uri
    self.model = model
    self.score_threshold = score_threshold
    self.width = frame_width
    self.height = frame_height
    self.rtmp_out = rtmp_out
    self.max_results = max_results
    try:
      self.webcam = Webcam(self.cam_uri, self.width, self.height)
    except OpenStreamException as e:
      return None
    self.ffmpeg = Ffmpeg(self.rtmp_out)
    self.ai_analyser = Ai_analyser(self.model, self.score_threshold, self.max_results)
    self.visualiser = Visualiser()

  def run(self):
    while self.webcam.is_open():
      start_time = round(time() * 1000)
      try:
        frame = self.webcam.read_frame()
        current_frame = frame
        frame = self.webcam.convert_to_rgb(frame)
        self.ai_analyser.add_image(frame)
        self.ai_analyser.detect()
        current_frame = self.visualiser.show_fps(current_frame,self.ai_analyser.get_fps())
        self.ai_analyser.render_result(self.visualiser, current_frame)
        self.ffmpeg.output_frame(current_frame)
      except WebcamReadException as wre:
        print(f'Error: {wre}')
        continue
      except NoImageInDetectorException as nid:
        print(f'Error {nid}')
        continue
      if (self.webcam.break_key() == 27):
        break
      end_time = round(time() * 1000)
      duration = (end_time - start_time) / 1000.0
      duration_diff = 0.125-duration
      if (duration_diff > 0 ):
        sleep(duration_diff);

    self.ai_analyser.terminate()
    self.ffmpeg.terminate()
    self.webcam.terminate()

if __name__ == '__main__':
  cam_uri = environ.get('CAM_URI')
  rtmp_out = environ.get('RTMP_OUT')
  score_threshold = float(environ.get('SCORE_THRESHOLD'))
  model = environ.get('MODEL')
  app = Application(cam_uri, model, score_threshold, 640, 360, rtmp_out, 5)
  if (app is not None):
    app.run()