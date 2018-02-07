from multiprocessing import Process, Pipe, Queue
from audioproc import AudioRecorder
from videoproc import VideoRecorder
import time

TRIGGER_HEADER = 'TRGR'

def run_audio_proc(pipe_endpt):
  rec = AudioRecorder()
  print("AudioRecorder ready")
  while (rec.waitForLoudNoise()):
    le_time = time.localtime()
    pipe_endpt.send([TRIGGER_HEADER,le_time])
  
def run_video_proc(pipe_endpt):
  rec = VideoRecorder()
  print("VideoRecorder ready")
  while (True):
    msg = pipe_endpt.recv()
    print(msg)
    if (msg[0] == TRIGGER_HEADER):
      rec.recordSegment()

def main():
  # create a pipe for the two subprocesses to commnicate on
  video_proc_endpt, audio_proc_endpt = Pipe()

  # create separate audio and video subprocesses 
  audio_proc = Process(target=run_audio_proc, args=((audio_proc_endpt),))
  audio_proc.start()
  
  video_proc = Process(target=run_video_proc, args=((video_proc_endpt),))
  video_proc.start()
  
  
if __name__ == '__main__':
  main()


