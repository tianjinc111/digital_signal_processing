# play_vibrato_interpolation.py
# Reads a specified wave file (mono) and plays it with a vibrato effect.
# (Sinusoidally time-varying delay)
# Uses linear interpolation

import pyaudio
import wave
import struct
import math
from myfunctions import clip16

from matplotlib import pyplot

#wavfile = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/class demo/demo 10 - vibrato/decay_cosine_mono.wav'
wavfile = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/class demo/demo 10 - vibrato/author.wav'
# wavfile = 'cosine_200_hz.wav'

print('Play the wave file: %s.' % wavfile)

# Open wave file
wf = wave.open( wavfile, 'rb')

BLOCKLEN = 64
# Read wave file properties
RATE        = wf.getframerate()     # Frame rate (frames/second)
WIDTH       = wf.getsampwidth()     # Number of bytes per sample
LEN         = wf.getnframes()       # Signal length
CHANNELS    = wf.getnchannels()     # Number of channels

print('The file has %d channel(s).'         % CHANNELS)
print('The file has %d frames/second.'      % RATE)
print('The file has %d frames.'             % LEN)
print('The file has %d bytes per sample.'   % WIDTH)

# Vibrato parameters
f0 = 2
W = 0.2   # W = 0 for no effect

# f0 = 2; W = 0.2

# OR
# f0 = 2
# ratio = 2.06
# W = (ratio - 1.0) / (2 * math.pi * f0 )
# print(W)

# Buffer to store past signal values. Initialize to zero.
BUFFER_LEN =  1024          # Set buffer length.
buffer = BUFFER_LEN * [0]   # list of zeros

# Buffer (delay line) indices
kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  # write index (initialize to middle of buffer)

print('The buffer is %d samples long.' % BUFFER_LEN)


[g2] = pyplot.plot([],[], 'red', label = 'Second')






n = range(0, BLOCKLEN)
pyplot.xlim(0, BLOCKLEN)         # set x-axis limits
pyplot.xlabel('Time (n)')
                # x-data of plot (discrete-time)
g2.set_xdata(n)                   # x-data of plot (discrete-time)
pyplot.legend()


pyplot.ylim(-10000, 10000)  

# Open an output audio stream
p = pyaudio.PyAudio()


PA_FORMAT = p.get_format_from_width(WIDTH)
#stream = p.open(
   # format = PA_FORMAT,
   # channels = CHANNELS,
   # rate = RATE,
   # input = True,
   # output = True,
   # frames_per_buffer = 256)   


stream = p.open(format      = pyaudio.paInt16,
                channels    = 1,
                rate        = RATE,
                input       = False,
                output      = True )

print ('* Playing...')
input_bytes = wf.readframes(BLOCKLEN)
n = 0
# Loop through wave file 
#for n in range(0, LEN):
while len(input_bytes) >= BLOCKLEN * WIDTH:
    # Convert string to number
    input_block = struct.unpack('h' * BLOCKLEN, input_bytes)
    for x0 in input_block:
        
        # Get previous and next buffer values (since kr is fractional)
        kr_prev = int(math.floor(kr))
        frac = kr - kr_prev    # 0 <= frac < 1
        kr_next = kr_prev + 1
        if kr_next == BUFFER_LEN:
            kr_next = 0

        # Compute output value using interpolation
        y0 = (1-frac) * buffer[kr_prev] + frac * buffer[kr_next]

        # Update buffer
        buffer[kw] = x0

        # Increment read index
        kr = kr + 1 + W * math.sin( 2 * math.pi * f0 * n / RATE )
            # Note: kr is fractional (not integer!)

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
        n = n + 1
    input_bytes = wf.readframes(BLOCKLEN)
print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()
wf.close()