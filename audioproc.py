import sounddevice as sd
import numpy as np
import time

class AudioRecorder:
  SAMPLE_FREQ = 44100
  TIME_WINDOW = 100

  def __init__(self, name="audioproc", pipe=None):
    self.name = name
    self.last_triggered = time.time()

  def __del__(self):
    pass

  def recordOne(self):
    duration = 0.1  # seconds
    samples = sd.rec(int(duration * self.SAMPLE_FREQ),  channels=1)
    sd.wait() # wait for recording to complete
    max_val = np.amax(samples)
    samples = None
    return (max_val)
    
  def waitForLoudNoise(self):
    while (True):
      peak_val = self.recordOne()
      if (peak_val > 0.5):
        print("peak_val: ", peak_val)  
        cur_time = time.time()
        dtime = cur_time - self.last_triggered
        if (dtime > 3):
          print(time.strftime("trigger at: %G%m%d%H%M%S",time.localtime()))          
          self.last_triggered = cur_time
          return True

def main():
  recorder = AudioRecorder()
  recorder.waitForLoudNoise()

if __name__ == '__main__':
  main()