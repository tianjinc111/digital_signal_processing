# echo_via_circular_buffer.py
# Reads a specified wave file (mono) and plays it with an echo.
# This implementation uses a circular buffer.

import pyaudio
import wave
import struct
from myfunctions import clip16

#wavfile = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/class demo/demo 08 - circular buffer/author.wav'




WIDTH       = 2         # Number of bytes per sample
CHANNELS    = 1         # mono
RATE        = 16000     # Sampling rate (frames/second)
DURATION    = 6         # duration of processing (seconds)

N = DURATION * RATE     # N : Number of samples to process





#'author.wav'

# Open the wave file




# Set parameters of delay system
b0 = 1.0            # direct-path gain
G = 0.8             # feed-forward gain
delay_sec = 0.05    # delay in seconds, 50 milliseconds   Try delay_sec = 0.02
N = int( RATE * delay_sec )   # delay in samples

print('The delay of %.3f seconds is %d samples.' %  (delay_sec, N))

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN = N              # length of buffer
buffer = BUFFER_LEN * [0]   # list of zeros

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)

# Get first frame


# Initialize buffer index (circular index)
k = 0

print('* Start')

while len(input_bytes) > 0:

    input_bytes = stream.read(1)

    # Convert binary data to number
    x0, = struct.unpack('h', input_bytes)

    # Compute output value
    # y(n) = b0 x(n) + G x(n-N)
    y0 = b0 * x0 + G * buffer[k]

    # Update buffer
    buffer[k] = x0

    # Increment buffer index
    k = k + 1
    if k >= BUFFER_LEN:
        # The index has reached the end of the buffer. Circle the index back to the front.
        k = 0

    # Clip and convert output value to binary data
    output_bytes = struct.pack('h', int(clip16(y0)))

    # Write output value to audio stream
    stream.write(output_bytes)

    # Get next frame
    input_bytes = wf.readframes(1)     

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()