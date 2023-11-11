# Tk_demo_04_slider.py
# TKinter demo
# Play a sinusoid using Pyaudio. Use two sliders to adjust the frequency and gain.

from math import cos, pi 
import pyaudio, struct
import tkinter as Tk    
import wave

def fun_quit():
  global CONTINUE
  print('Good bye')
  CONTINUE = False


def clip16(x):
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    return (x)



## basic variables of input audio

input_wf = wave.open('/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/testing zgm/Q1.wav', 'rb')
RATE = input_wf.getframerate()
WIDTH = input_wf.getsampwidth()
LEN = input_wf.getnframes()
CHANNELS = input_wf.getnchannels()
print(f"rate: {RATE}, width: {WIDTH}, len: {LEN}, ch: {CHANNELS}")
output_wf = wave.open('output_Q1.wav', 'w')
output_wf.setnchannels(CHANNELS)
output_wf.setsampwidth(WIDTH)
output_wf.setframerate(RATE)



# %%
# Buffer
BUFFER_LEN = int(RATE * 0.03)
buffer = BUFFER_LEN * [0]  # initialize to zero
# Buffer indices
kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  # write index
print(f"buffer len: {BUFFER_LEN}")



# %%



Fs = 8000     # rate (samples/second)
gain = 0.2 * 2**15

# Define Tkinter root
root = Tk.Tk()

# Define Tk variables
f1 = Tk.DoubleVar()
gain = Tk.DoubleVar()

# Initialize Tk variables
f1.set(200)   # f1 : frequency of sinusoid (Hz)
gain.set(0.2 * 2**15)

# Define widgets
S_freq = Tk.Scale(root, label = 'Frequency', variable = f1, from_ = 100, to = 400, tickinterval = 100)
S_gain = Tk.Scale(root, label = 'Gain', variable = gain, from_ = 0, to = 2**15-1)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

# Place widgets
B_quit.pack(side = Tk.BOTTOM, fill = Tk.X)
S_freq.pack(side = Tk.LEFT)
S_gain.pack(side = Tk.LEFT)

# Create Pyaudio object
# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True)        
  # specify low frames_per_buffer to reduce latency

BLOCKLEN = 256
output_block = [0] * BLOCKLEN
theta = 0
CONTINUE = True
prev = 0
import math
print('* Start')
while CONTINUE:

  n = 0
  cur = gain.get()
  # root.update()
  om1 = 2.0 * pi * f1.get() / Fs
  once_gain = (cur - prev) / BLOCKLEN


  input_bytes = input_wf.readframes(1)

  x0, = struct.unpack('h', input_bytes)  # Convert string to number
    # Get buffer values
  kr_prev = int(math.floor(kr))
  frac = kr - kr_prev  # 0 <= frac < 1
  kr_next = kr_prev + 3

  if kr_next == BUFFER_LEN:
    kr_next = 0

  y0 = x0 + cur * ((1 - frac) * buffer[kr_prev] + frac * buffer[kr_next])  # 2.29

  buffer[kw] = x0


  kr = kr + 1 + 0.2 * math.sin(2 * math.pi * f1.get() * n / RATE) 

  n += 1


  # for i in range(0, BLOCKLEN):
  #   output_block[i] = int( (prev + once_gain * (i + 1)) * cos(theta) )
  #   theta = theta + om1
  prev = cur
  # if theta > pi:
  #   theta = theta - 2.0 * pi

  # Ensure that 0 <= kr < BUFFER_LEN
  if kr >= BUFFER_LEN:
        # End of buffer. Circle back to front.
        kr = kr - BUFFER_LEN
    # Increment write index
  kw = kw + 1
  if kw == BUFFER_LEN:
        # End of buffer. Circle back to front.
        kw = 0
    # Clip and convert output value to binary data
  output_bytes = struct.pack('h', int(clip16(y0)))
    # Write output to audio stream
  stream.write(output_bytes)



  binary_data = struct.pack('h' * BLOCKLEN, *output_block)   # 'h' for 16 bits
  stream.write(binary_data)
  output_wf.writeframes(output_bytes)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
