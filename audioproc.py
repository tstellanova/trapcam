#!/usr/bin/env python

import sounddevice as sd
import numpy as np
import time

class AudioRecorder:
  SAMPLE_FREQ = 44100
  LOUD_NOISE_THRESHOLD = 0.5
  LOUD_NOISE_DELAY_SECS = 3 # time between loud noises

  def __init__(self, name="audioproc", pipe=None):
    self.name = name
    self.last_triggered = time.time()

  def __del__(self):
    pass

  def recordOne(self):
    duration = 0.1  # seconds
    # block until recording finishes
    samples = sd.rec(int(duration * self.SAMPLE_FREQ),  channels=1, blocking=True)
    max_val = np.amax(samples)
    samples = None
    return (max_val)
    
  def waitForLoudNoise(self):
    while (True):
      peak_val = self.recordOne()
      if (peak_val > self.LOUD_NOISE_THRESHOLD):
        # print("peak_val: ", peak_val)
        cur_time = time.time()
        dtime = cur_time - self.last_triggered
        if (dtime > self.LOUD_NOISE_DELAY_SECS):
          # print(time.strftime("trigger at: %G%m%d%H%M%S",time.localtime()))
          self.last_triggered = cur_time
          return True

def main():
  recorder = AudioRecorder()
  recorder.waitForLoudNoise()

if __name__ == '__main__':
  main()