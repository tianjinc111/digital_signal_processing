import pyaudio, struct
import wave, math
from math import cos, pi 
import tkinter as Tk   
from myfunctions import clip16

def fun_quit():
  global CONTINUE
  print('Good bye')
  CONTINUE = False

wavfile = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/testing zgm/origin.wav'
# Open wave file
wf = wave.open( wavfile, 'rb')

# Read wave file properties
RATE        = wf.getframerate()     # Frame rate (frames/second)
WIDTH       = wf.getsampwidth()     # Number of bytes per sample
LEN         = wf.getnframes()       # Signal length
CHANNELS    = wf.getnchannels()     # Number of channels

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

wavfile_output = 'q1.wav'
wf_output = wave.open(wavfile_output, 'w')
wf_output.setframerate(RATE)      # Sampling rate (frames/second)
wf_output.setnchannels(CHANNELS)  # Number of channels
wf_output.setsampwidth(WIDTH)     # Number of bytes per sample



# Create a buffer (delay line) for past values
BUFFER_LEN =  256         # Buffer length
buffer = BUFFER_LEN*[0]   # Initialize to zero

# Buffer (delay line) indices
kw = 0  # read index
kr = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)



# Define Tkinter root
root = Tk.Tk()

# Define Tk variables
freq = Tk.DoubleVar()
swee = Tk.DoubleVar()
gain = Tk.DoubleVar()

# Initialize Tk variables
freq.set(0)   # f1 : frequency of sinusoid (Hz)
swee.set(0)
gain.set(0)

# Define widgets
S_freq = Tk.Scale(root, label = 'Frequency', variable = freq, from_ = 0, to = 800, tickinterval = 100)
S_swee = Tk.Scale(root, label = 'Sweep Depth', variable = swee, from_ = 0, to = 10, tickinterval = 0.5)
S_gain = Tk.Scale(root, label = 'Gain', variable = gain, from_ = 0, to = 10, tickinterval = 1)
B_quit = Tk.Button(root, text = 'Quit', command = fun_quit)

# Place widgets
B_quit.pack(side = Tk.BOTTOM, fill = Tk.X)
S_freq.pack(side = Tk.LEFT)
S_swee.pack(side = Tk.RIGHT)
S_gain.pack(side = Tk.LEFT)


# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(
    format      = pyaudio.paInt16,
    channels    = 1,
    rate        = RATE,
    input       = False,
    output      = True, 
    frames_per_buffer = 256)

CONTINUE = True
# Loop through wave file 
for n in range(0, LEN):
    if not CONTINUE:
        break

    root.update()

    g = gain.get()  # gain
    f0 = freq.get()  # LFO frequency
    W = swee.get()  # LFO sweep depth

    # Get sample from wave file
    input_bytes = wf.readframes(1)  # get sample from wav
    x0, = struct.unpack('h', input_bytes)  # Convert string to number

    # Get buffer values
    kr_prev = int(math.floor(kr))
    frac = kr - kr_prev  # 0 <= frac < 1
    kr_next = kr_prev + 1

    if kr_next == BUFFER_LEN:
        kr_next = 0

    # Compute output value using interpolation
    y0 = x0 + g * ((1 - frac) * buffer[kr_prev] + frac * buffer[kr_next])

    # Update buffer
    buffer[kw] = x0
    # Increment read index
    kr = kr + 1 + W * math.sin(2 * math.pi * f0  * n / RATE)

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
    wf_output.writeframes(output_bytes)


stream.stop_stream()
stream.close()
p.terminate()
wf.close()