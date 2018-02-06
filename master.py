from multiprocessing import Process, Pipe, Queue
from audioproc import AudioRecorder
from videoproc import VideoRecorder
import time

TRIGGER_HEADER = 'TRGR'

def run_audio_proc(pipe_endpt):
  rec = AudioRecorder()
  while (rec.waitForLoudNoise()):
    pipe_endpt.send([TRIGGER_HEADER,time.localtime()])
  
def run_video_proc(pipe_endpt):
  rec = VideoRecorder()
  while (True):
    msg = pipe_endpt.recv()
    if (msg[0] == TRIGGER_HEADER):
      rec.recordSegment()

def main():
  # create a pipe for the two subprocesses to commnicate on
  video_proc_endpt, audio_proc_endpt = Pipe()

  audio_proc = Process(target=run_audio_proc, args=((audio_proc_endpt),))
  audio_proc.start()
  
  video_proc = Process(target=run_video_proc, args=((video_proc_endpt),))
  video_proc.start()
  
  
if __name__ == '__main__':
  main()


