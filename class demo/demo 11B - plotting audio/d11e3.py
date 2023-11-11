# plot_microphone_input.py

import pyaudio
import struct
from matplotlib import pyplot

WIDTH = 2           # bytes per sample
CHANNELS = 1        # mono
RATE = 8000         # frames per second
BLOCKLEN = 1024     # block length in samples
DURATION = 10       # Duration in seconds

K = int( DURATION * RATE / BLOCKLEN )   # Number of blocks

print('Block length: %d' % BLOCKLEN)
print('Number of blocks to read: %d' % K)
print('Duration of block in milliseconds: %.1f' % (1000.0 * BLOCKLEN/RATE))

# Set up plotting...

pyplot.ion()           # Turn on interactive mode
pyplot.figure(1)
# [g1] = pyplot.plot([], [], 'blue')  # Create empty line

[g1] = pyplot.plot([], [], 'blue', label='Input Signal')
[g2] = pyplot.plot([], [], 'red', label='Output signal')

n = range(0, BLOCKLEN)
pyplot.xlim(0, BLOCKLEN)         # set x-axis limits
pyplot.xlabel('Time (n)')
g1.set_xdata(n)                   # x-data of plot (discrete-time)
g2.set_xdata(n)

# --- Time axis in units of milliseconds ---
# t = [n*1000/float(RATE) for n in range(BLOCKLEN)]
# pyplot.xlim(0, 1000.0 * BLOCKLEN/RATE)         # set x-axis limits
# pyplot.xlabel('Time (msec)')
# g1.set_xdata(t)                   # x-data of plot (time)

pyplot.ylim(-10000, 10000)        # set y-axis limits

# Open the audio stream

p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(
    format = PA_FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = 256)

output_block = BLOCKLEN * [0]

# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829

# Initialization
x1 = 0.0
x2 = 0.0
x3 = 0.0
x4 = 0.0
y1 = 0.0
y2 = 0.0
y3 = 0.0
y4 = 0.0

# Read microphone, plot audio signal

for i in range(K):

    # Read audio input stream
    input_bytes = stream.read(BLOCKLEN)

    # In case of run-time errors, try using instead:
    # input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)

    signal_block = struct.unpack('h' * BLOCKLEN, input_bytes)  # Convert
    
    for j in range(BLOCKLEN):
        x0 = signal_block[j]
        
        # Difference equation
        y0 = b0*x0 + b2*x2 + b4*x4 - a1*y1 - a2*y2 - a3*y3 - a4*y4

        # Delays
        x4 = x3
        x3 = x2
        x2 = x1
        x1 = x0
        y4 = y3
        y3 = y2
        y2 = y1
        y1 = y0
        
        output_block[j] = int(y0)

    g1.set_ydata(signal_block)   # Update y-data of plot
    g2.set_ydata(output_block)
    pyplot.pause(0.0001)

    # Convert output value to binary data
    output_bytes = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio stream
    stream.write(output_bytes)


stream.stop_stream()
stream.close()
p.terminate()

pyplot.ioff()           # Turn off interactive mode
pyplot.show()           # Keep plot showing at end of program
pyplot.close()

print('-- Finished')