import uvc
import logging
import time
logging.basicConfig(level=logging.INFO)

SEGMENT_FRAMES=60
FILMING_MINUTES = 20
FILMING_SECONDS = int(FILMING_MINUTES * 60) 
FILM_DURATION_SECONDS = 30
FPS = 30
TOTAL_FRAMES = int(FPS * FILM_DURATION_SECONDS) 
INTERFRAME_DELAY_SECS = float(FILMING_SECONDS/TOTAL_FRAMES) 


class VideoRecorder:
  capture = None
  
  def __init__(self, name="videoproc", pipe=None):
    self.name = name
    self.setup()

  def __del__(self):
    self.capture = None
        
        
  def generateTimeFilename(self):
    timestamp = time.strftime("%G%m%d%H%M%S",time.localtime())
    fname = "{0}-vid.mjpeg".format(timestamp)
    return fname
    
  def openOutputFile(self):
    fname = self.generateTimeFilename()
    fd = open(fname ,"ab+")
    print("out file open " , fname)
    return fd

  def setup(self):
    dev_list =  uvc.device_list()
    # print("devices: ", dev_list)
    cap = uvc.Capture(dev_list[0]['uid'])
    #print("modes: ",  cap.avaible_modes)
    #print(dir(cap))

    cap.frame_mode = (1920, 1080, 30)

    # grab one frame to fully spin-up camera
    frame = cap.get_frame_robust()
    self.capture = cap
    frame = None
    
  def recordSegment(self,nframes=SEGMENT_FRAMES):
    """Record the given frames as quickly as possible.
    """
    print("recordSegment ", nframes)
    fname = self.generateTimeFilename()
    with (open(fname ,"ab+")) as fd:
      print("out file open " , fname)
      for i in range(nframes):
        frame = self.capture.get_frame_robust()
        fd.write(frame.jpeg_buffer)

      fd.flush()
      fd.close()

def main():
  rec = VideoRecorder()
  rec.recordSegment(TOTAL_FRAMES)
  print("done writing")


if __name__ == '__main__':
  main()