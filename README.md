# easyFFT
Simple Audio Analysis and Display Utility
![easyFFT Screenshot][easyFFT.png]

## Background
This is my proof of concept sound analysis / signal processing tool that I wrote in support of my larger project to train a neural network to identify audio signatures from aircraft. easyFFT was developed on an Nvidia Jetson TX2 board with a Mircrosoft USB Lifecam Cinema for the mic input.

## Usage
It is likely that the capture settings will need to be updated to match your hardware, especially the device. I believe the other capture settings should work for most modern microphones. To determine the location of your microphone/input device, run <b> alrecord -l</b> and replace the DEVICE setting with hw:X,Y for your device, where X=Card #, and Y = Subdevice #.

### Dependencies
The following python libraries will need to be installed via pip or other. I list the version below that I have tested with, but later versions should work as well. easyFFT was developed on Python 3.5.2

 * alsaaudio  (pyalsaaudio) v. 0.8.4
 * matplotlib (matplotlib)  v. 2.2.2
 * numpy      (numpy)       v. 1.14.2

### Default Audio settings
```
capset = {
        'TYPE'    : alsaaudio.PCM_CAPTURE,
        'MODE'    : alsaaudio.PCM_NORMAL,
        'FORMAT'  : alsaaudio.PCM_FORMAT_S16_LE,
        'DEVICE'  : 'hw:2,0',
        'CHANNELS': 1,
        'RATE'    : 44100,
        'PERIODSZ': 2048, 
        'SAMPLESZ':.1
        }
```
#### Running
After updating necessary settings for your hardware run the easyFFT.py script. Since the goal is not to capture audio for playback, dropped frames are okay, but if you see them excessively it may indicate your capture window is too small ('SAMPLESZ') or that your capture rate is too high ('RATE'). If exceptions are thrown, you may need to lower/adjust the PERIODSZ as well.

### Exiting
Press 'Enter' key to terminate program.
