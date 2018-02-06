import uvc
import logging
import time
import os
logging.basicConfig(level=logging.INFO)

SEGMENT_FRAMES=60
FILMING_MINUTES = 20
FILMING_SECONDS = int(FILMING_MINUTES * 60) 
FILM_DURATION_SECONDS = 30
FPS = 10
TOTAL_FRAMES = int(FPS * FILM_DURATION_SECONDS) 
INTERFRAME_DELAY_SECS = float(FILMING_SECONDS/TOTAL_FRAMES) 


class VideoRecorder:
  capture = None
  
  def __init__(self, name="videoproc", pipe=None):
    self.name = name
    self.temp_file_name = None
    self.setup()

  def __del__(self):
    self.capture = None
    self.fd = None
        
        
  def generateTimeFilename(self):
    timestamp = time.strftime("%G%m%d%H%M%S",time.localtime())
    fname = "{0}-vid.mjpeg".format(timestamp)
    return fname
    
  def openTempFile(self):
    self.temp_file_name = self.generateTimeFilename()
    self.fd = open(self.temp_file_name ,"ab+")
    print("temp file open " , self.temp_file_name )

  def setup(self):
    dev_list =  uvc.device_list()
    # print("devices: ", dev_list)
    cap = uvc.Capture(dev_list[0]['uid'])
    #print("modes: ",  cap.avaible_modes)
    print(dir(cap))

    frame = None
    cap.frame_mode = (1920, 1080, 30)

    frame = cap.get_frame_robust()
    time.sleep(3)
    frame = None
  
    self.capture = cap
    self.openTempFile()
    
  def recordSegment(self,nframes=SEGMENT_FRAMES):
    """Record the given frames as quickly as possible.
    """
    for i in range(nframes):
      frame = self.capture.get_frame_robust()
      self.fd.write(frame.jpeg_buffer)

    self.fd.flush()
    self.fd.close()
    self.fd = None
    
    new_fname = generateTimeFilename()
    print("move {0} to {1}".format(self.temp_file_name, new_fname))
    os.rename(self.temp_file_name, new_fname)
    self.temp_file_name = None
    # pre-open a new temp file for video recording
    self.openTempFile()

def main():
  rec = VideoRecorder()
  rec.recordSegment(TOTAL_FRAMES)
  print("done writing")


if __name__ == '__main__':
  main()