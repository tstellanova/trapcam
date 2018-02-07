#!/usr/bin/env python

from multiprocessing import Process, Pipe, Queue
from audioproc import AudioRecorder
from videoproc import VideoRecorder
import time

TRIGGER_HEADER = 'TRGR'

def run_audio_proc(pipe_endpt):
  """ Run audio monitor in its own process
  """
  rec = AudioRecorder()
  print("AudioRecorder ready")
  while (rec.waitForLoudNoise()):
    # send a trigger message
    le_time = time.localtime()
    pipe_endpt.send([TRIGGER_HEADER,le_time])
  
def run_video_proc(pipe_endpt):
  """ Run video capture in its own process
  """
  rec = VideoRecorder()
  print("VideoRecorder ready")
  while (True):
    # wait for a trigger message from the audio monitor
    msg = pipe_endpt.recv()
    print(msg)
    if (msg[0] == TRIGGER_HEADER):
      rec.recordSegment()

def main():
  # create a pipe for the two subprocesses to commnicate with
  video_proc_endpt, audio_proc_endpt = Pipe()

  # create and start separate audio and video subprocesses 
  audio_proc = Process(target=run_audio_proc, args=((audio_proc_endpt),))
  audio_proc.start()
  
  video_proc = Process(target=run_video_proc, args=((video_proc_endpt),))
  video_proc.start()
  
  
if __name__ == '__main__':
  main()


