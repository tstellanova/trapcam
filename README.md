# trapcam

Experimental camera trap for linux mini computers such as Raspberry Pi, ODROID, Orange Pi, and similar.

- Requires a USB webcam that provides MJPEG and has a microphone for audio input. One example is the Logitech HD Webcam C525.
- Depends on `libuvc` and PortAudio.  

### Purpose

My intent was to capture short video clips of a frequent loud event in our neighborhood.
The idea was that whenever the loud event happens, we can use the webcam's microphone to detect
the event and trigger the camera.

### Method

I wanted to capture video as close in time to the lound sound event.
In order to do this, we power up the video camera at the start of the program and wait for
the audio process to detect a loud sound.  
When the audio process detects a loud sound, it sends a message via a pipe to the video process,
which then immediately captures a short video clip and saves it.  

#### Multiprocessing

We use python multiprocessing to keep the audio and video capture running in separate (child) processes.
You could do all of the work in a single process or using eg python threads.
Since the mini computer I used has multiple cores, I opted to take advantage of them. 


## Setup

Depending on your linux configuration you may need to install various audio and video libraries.

- [Setup sounddevice audio capture on Raspberry Pi 3] (https://gist.github.com/tstellanova/11ef60480552e2c5660af8e9e14410c8)
- [Setup libuvc video capture on Raspberry Pi 3](https://gist.github.com/tstellanova/1bd93b82f9f9fbc57c7c503a54514d6d)
- Connect a webcam to your mini computer
- Run `python3 master.py` and make a loud noise in front of the camera

## Results

Typically we're able to capture a frame or two of video from before the audio trigger happens, 
then the moment when the trigger happens,
and then some number of frames after the trigger. 
Although we don't send the trigger message to the video process until after the audio event happens,
the video capture driver is actually constantly receiving a video stream from the camera 
and some arbitrary amount of buffered video data is captured at the moment the trigger is sent. 
Your mileage may vary depending on the specific webcam, linux distribution, and mini computer hardware you're using. 

### Further work / customization

- As configured, the audio process ignores loud noises that happen within a 3-second window after the most recent loud noise. This is an arbitrary setting to "debounce" the triggering noise. 
- We don't currently save the audio with the video. It might be possible to save the audio clips and then add them as an audio track with eg ffmpeg.
- We're sending the timestamp of the audio trigger event to the video process. This could be used to fine-tune the video capture control, if we're concerned about audio trigger events arriving faster than the video process can capture.
- The video camera is constantly powered up. If you're installing a camera trap in a remote location on eg battery power, you might find this burns too much power.  You could modify the video recorder to only create a new Capture (`cap = uvc.Capture`) when triggered.  This means there would be a much longer delay between the audio trigger and the start of video capture-- but maybe that's OK for your purpose.


