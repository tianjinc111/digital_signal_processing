# plot_microphone_input_spectrum.py
"""
Using Pyaudio, get audio input and plot real-time FFT of blocks.
Ivan Selesnick, October 2015
Based on program by Gerald Schuller
"""

import pyaudio
import struct
from matplotlib import pyplot as plt
import numpy as np
from math import cos, pi

plt.ion()  # Turn on interactive mode so plot gets updated

WIDTH = 2  # bytes per sample
CHANNELS = 1  # mono
RATE = 8000  # Sampling rate (samples/second)
BLOCKSIZE = 1024  # length of block (samples)
DURATION = 8  # Duration (seconds)

f0 = 400
om = 2.0 * pi * f0 / RATE
theta = 0

output_block = [0] * BLOCKSIZE

NumBlocks = int(DURATION * RATE / BLOCKSIZE)

print('BLOCKSIZE =', BLOCKSIZE)
print('NumBlocks =', NumBlocks)
print('Running for ', DURATION, 'seconds...')

DBscale = False
# DBscale = True

# Initialize plot window:
plt.figure(1)
if DBscale:
    plt.ylim(0, 150)
else:
    plt.ylim(0, 20 * RATE)

# Frequency ax1is (Hz)
plt.xlim(0, 0.5 * RATE)  # set x-axis limits
# plt.xlim(0, 2000)         # set x-axis limits
plt.xlabel('Frequency (Hz)')
f = RATE / BLOCKSIZE * np.arange(0, BLOCKSIZE)

line_input, = plt.plot([], [], color='blue', label='input')  # Create empty line
line_input.set_xdata(f)  # x-data of plot (frequency)
line_output, = plt.plot([], [], color='red', label='output')  # Create empty line
line_output.set_xdata(f)  # x-data of plot (frequency)
plt.legend()

# Open audio device:
p = pyaudio.PyAudio()
PA_FORMAT = p.get_format_from_width(WIDTH)

stream = p.open(format=PA_FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True)

for i in range(0, NumBlocks):
    input_bytes = stream.read(BLOCKSIZE)  # Read audio input stream
    input_tuple = struct.unpack('h' * BLOCKSIZE, input_bytes)  # Convert

    for i in range(0, BLOCKSIZE):
        output_block[i] = int(input_tuple[i] * cos(theta))
        theta = theta + om
    if theta > pi:
        theta = theta - 2 * pi

    X1 = np.fft.fft(input_tuple)
    X2 = np.fft.fft(output_block)

    # Update y-data of plot
    if DBscale:
        line_input.set_ydata(20 * np.log10(np.abs(X1)))
        line_output.set_ydata(20 * np.log10(np.abs(X2)))
    else:
        line_input.set_ydata(np.abs(X1))
        line_output.set_ydata(np.abs(X2))
    plt.pause(0.001)
    # plt.draw()

    output_bytes = struct.pack('h' * BLOCKSIZE, *output_block)
    stream.write(output_bytes)

plt.close()

stream.stop_stream()
stream.close()
p.terminate()

print('* Finished')
