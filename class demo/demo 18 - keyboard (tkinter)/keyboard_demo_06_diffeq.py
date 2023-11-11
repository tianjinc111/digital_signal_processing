# keyboard_demo_06.py
# Play a note using a second-order difference equation
# when the user presses a key on the keyboard.

from ast import Continue
import pyaudio, struct
import numpy as np
from scipy import signal
from math import sin, cos, pi
import tkinter as Tk    

BLOCKLEN   = 64        # Number of frames per block
WIDTH       = 2         # Bytes per sample
CHANNELS    = 1         # Mono
RATE        = 8000      # Frames per second

MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Parameters
Ta = 2      # Decay time (seconds)

f0 = 440    # Frequency (Hz)
freqs = [0 for i in range(12)]
om = [0 for i in range(12)] 
a = [0,0,0] * 12
print(a)
b = [0] * 12




# Pole radius and angle
r = 0.01**(1.0/(Ta*RATE))       # 0.01 for 1 percent amplitude
# om1 = 2.0 * pi * float(f1)/RATE




# # Filter coefficients (second-order IIR)
# a = [1, -2*r*cos(om1), r**2]
# b = [r*sin(om1)]
i = 0
while i < 12:
    freqs[i] = 2 ** (i/12) * f0
    om[i] = 2.0 * pi * float(freqs[i])/RATE
    a[i] = [1, -2*r*cos(om[i]), r**2]
    b[i] = [r*sin(om[i])]
    i += 1

print(freqs)




ORDER = 2   # filter order


states = [np.zeros(ORDER) for i in range(12)]
x = [np.zeros(BLOCKLEN) for i in range(12)]
y = [0 for i in range(12)] 

# states = np.zeros(ORDER)
# x = np.zeros(BLOCKLEN)

# Open the audio output stream
p = pyaudio.PyAudio()
PA_FORMAT = pyaudio.paInt16
stream = p.open(
        format      = PA_FORMAT,
        channels    = CHANNELS,
        rate        = RATE,
        input       = False,
        output      = True,
        frames_per_buffer = 128)
# specify low frames_per_buffer to reduce latency
 
CONTINUE = True
# KEYPRESS = False

KEYPRESS = [False] * 12

def my_function(event):
    global CONTINUE
    global KEYPRESS
    print('You pressed ' + event.char)

    
    if event.char == 'q':
      print('Good bye')
      CONTINUE = False

    elif event.char == 'a':
        KEYPRESS[0] = True
    elif event.char == 'w':
        KEYPRESS[1] = True
    elif event.char == 'e':
        KEYPRESS[2] = True
    elif event.char == 'r':
        KEYPRESS[3] = True
    elif event.char == 't':
        KEYPRESS[4] = True
    elif event.char == 'y':
        KEYPRESS[5] = True
    elif event.char == 'u':
        KEYPRESS[6] = True
    elif event.char == 'i':
        KEYPRESS[7] = True
    elif event.char == 'o':
        KEYPRESS[8] = True
    elif event.char == 'p':
        KEYPRESS[9] = True
    elif event.char == '[':
        KEYPRESS[10] = True
    elif event.char == ']':
        KEYPRESS[11] = True
    

root = Tk.Tk()
root.bind("<Key>", my_function)

print('Press a w e r t y u i o p [ ] for sound.')
print('Press "q" to quit')

while CONTINUE:
    root.update()

        # if KEYPRESS and CONTINUE:
    #     # Some key (not 'q') was pressed
    #     x[0] = 10000.0

   
    # [y, states] = signal.lfilter(b, a, x, zi = states)

    # x[0] = 0.0        
    # KEYPRESS = False


    for i in range(12):

        if KEYPRESS[i] and CONTINUE:

            x[i][0] = 10000.0


        [y[i], states[i]] = signal.lfilter(b[i], a[i], x[i], zi = states[i])
        x[i][0] = 0.0        
        KEYPRESS[i] = False
        y[i] = np.clip(y[i].astype(int), -MAXVALUE, MAXVALUE) 


    ytotal = y[0] + y[1] + y[2] + y[3] + y[4] + y[5] + y[6] + y[7] + y[8] + y[9] + y[10] + y[11]
    #y = np.clip(y.astype(int), -MAXVALUE, MAXVALUE)     # Clipping
    ytotal = np.clip(ytotal.astype(int), -MAXVALUE, MAXVALUE)
    binary_data = struct.pack('h' * BLOCKLEN, *ytotal);    # Convert to binary binary data
    stream.write(binary_data, BLOCKLEN)               # Write binary binary data to audio output

print('* Done.')

# Close audio stream
stream.stop_stream()
stream.close()
p.terminate()
