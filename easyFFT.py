#!/usr/bin/python3
#!/usr/bin/python3

#import struct 
from struct import unpack as unpack
import alsaaudio
import _thread as thread
from time import time as time
import matplotlib.pyplot as plt
import numpy as np

# Audio settings
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

inp = alsaaudio.PCM(capset['TYPE'], capset['MODE'], capset['DEVICE']) 
inp.setchannels(capset['CHANNELS'])
inp.setrate(capset['RATE'])
inp.setformat(capset['FORMAT'])
inp.setperiodsize(capset['PERIODSZ'])

# Set up plots
freq_plt = plt.subplot(212)
time_plt = plt.subplot(211)
plt.ion()
plt.show()

# Calculate the number of datapoints we will have in a sample
x = np.arange( ( (capset['RATE'] * capset['SAMPLESZ']) //
                 (capset['PERIODSZ']) + 
                 ( (capset['RATE'] * capset['SAMPLESZ']) %
                  capset['PERIODSZ'] > 0) ) * capset['PERIODSZ'] )

print("<----- PRESS ENTER KEY IN THIS TERMINAL TO TERMINATE PROCSSING ----->")
print("Lossless capture rate will be %d frames"%(len(x),))

init_ary = np.zeros(len(x))
time_line, = time_plt.plot(x, init_ary, 'b')
freq_line, = freq_plt.plot(x, init_ary, 'r')
freq_plt.set_ylim(-100,10000)
freq_plt.set_xlim(0, 20000)
time_plt.set_ylim(-1,1)
time_plt.set_xlim(0,200)

# Thread to watch for 'Enter' press
#
def kb_thread(run):
    input()
    run.pop() 

run = [True]
audio_in = [] 
thread.start_new_thread(kb_thread, (run,))

# Thread to collect Audio data
# 
def rec_thread(run, inp, audio_in, settings, xlen):
    local_buf = []
    while run:
        while settings['SAMPLESZ'] > len(local_buf)/settings['RATE']:
            l, data = inp.read()
            if l:
                local_buf.extend([unpack('h', data[i:i+2])[0] for i in range(0,2*l,2)])
        audio_in.extend(local_buf)    
        if len(audio_in) > xlen :
            print("Dropped %d frames at %f"%(len(audio_in), time()))
        local_buf.clear()

thread.start_new_thread(rec_thread, (run, inp, audio_in, capset, len(x)))


while run:
    if audio_in:
        normal_audio = np.array(audio_in)/2.**15
        n = len(normal_audio)
        Nn = np.fft.fft(normal_audio)
        f_ind = np.arange(1, n//2)
        psd = abs(Nn[f_ind]**2) + abs(Nn[-f_ind]**2)
        freqs = np.fft.fftfreq(n, 1/capset['RATE'])
        freq_line.set_xdata(freqs[f_ind])
        freq_line.set_ydata(psd)
        time_line.set_xdata(np.arange(0, 1000, 1000/n ))
        time_line.set_ydata(normal_audio)
        plt.pause(0.001)
        audio_in.clear()

inp = None      

