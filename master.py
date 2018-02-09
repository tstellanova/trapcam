#!/usr/bin/env python

from multiprocessing import Process, Pipe, Queue
from audioproc import AudioRecorder
from videoproc import VideoRecorder
import time
import signal

TRIGGER_HEADER = 'TRGR'

def run_audio_proc(pipe_endpt):
  """ Run audio monitor in its own process
  """    
  rec = AudioRecorder()
  print("audioproc ready")
  try:
    while (rec.waitForLoudNoise()):
      # send a trigger message
      le_time = time.localtime()
      pipe_endpt.send([TRIGGER_HEADER,le_time])
  except KeyboardInterrupt:
    print("audioproc KeyboardInterrupt")
    
  rec = None
  pipe_endpt = None
  print("audioproc done")
  
  
def run_video_proc(pipe_endpt):
  """ Run video capture in its own process
  """
  rec = VideoRecorder()
  print("videoproc ready")
  try:
    while (True):
      # wait for a trigger message from the audio monitor
      msg = pipe_endpt.recv()
      print(msg)
      if (msg[0] == TRIGGER_HEADER):
        rec.recordSegment()
  except KeyboardInterrupt:
    print("videoproc KeyboardInterrupt")
    
  rec = None
  pipe_endpt = None
  print("videoproc done")
  
    
def main():
  # create a pipe for the two subprocesses to commnicate with
  video_proc_endpt, audio_proc_endpt = Pipe()

  # create and start separate audio and video subprocesses 
  audio_proc = Process(target=run_audio_proc, args=((audio_proc_endpt),))
  audio_proc.start()
  
  video_proc = Process(target=run_video_proc, args=((video_proc_endpt),))
  video_proc.start()
  
  try:
    audio_proc.join()
    video_proc.join()
  except KeyboardInterrupt:
    print("master KeyboardInterrupt") 
  
if __name__ == '__main__':
  main()


