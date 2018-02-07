#!/usr/bin/env python

import uvc
import logging
import time
logging.basicConfig(level=logging.INFO)

SEGMENT_FRAMES=15
FPS = 30


class VideoRecorder:
  capture = None
  
  def __init__(self, name="videoproc", pipe=None):
    self.name = name
    self.setup()

  def __del__(self):
    self.capture = None
        
        
  def generateTimestampFilename(self):
    timestamp = time.strftime("%G%m%d%H%M%S",time.localtime())
    fname = "{0}-vid.mjpeg".format(timestamp)
    return fname
    
  def openOutputFile(self):
    fname = self.generateTimestampFilename()
    fd = open(fname ,"ab+")
    print("out file open " , fname)
    return fd

  def setup(self):
    """Turn on the camera and be ready to capture video when asked.
    """
    dev_list =  uvc.device_list()
    # print("devices: ", dev_list)
    print("video device 0: " , dev_list[0])
    cap = uvc.Capture(dev_list[0]['uid'])
    # print("modes: ",  cap.avaible_modes)
    # print(dir(cap))
    # print(dir(cap.controls))
    for counter, value in enumerate(cap.controls):
      print(counter,value)

    # cap.frame_mode = (1920, 1080, 30)
    cap.frame_mode = (640, 480, 30)

    # grab one frame to fully spin-up camera
    frame = cap.get_frame_robust()
    self.capture = cap
    frame = None
    
  def recordSegment(self,nframes=SEGMENT_FRAMES):
    """Record the given frames as quickly as possible.
    """
    print("recordSegment ", nframes)
    fname = self.generateTimestampFilename()
    with (open(fname ,"ab+")) as fd:
      print("out file open " , fname)
      for i in range(nframes):
        frame = self.capture.get_frame_robust()
        fd.write(frame.jpeg_buffer)

      fd.flush()
      fd.close()

def main():
  rec = VideoRecorder()
  rec.recordSegment()
  print("done recording")

if __name__ == '__main__':
  main()