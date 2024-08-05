import subprocess as sp

class Ffmpeg:
  def __init__(self, rtmp_uri):
    self.rtmp_uri = rtmp_uri
    command = ['ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', '640x360',
        '-r', '8',
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-g', '10',
        '-bf', '2', 
        '-mpv_flags', 'strict_gop',
        '-preset', 'ultrafast',
        '-f', 'flv',
        self.rtmp_uri]
    self.proc = sp.Popen(command, stdin=sp.PIPE,shell=False)

  def terminate(self):
    if (self.proc is not None):
      self.proc.terminate()

  def get_stdin_pipe(self):
    return self.proc.stdin