# demo_filter_blocks_corrected.py
# Block filtering of a wave file, save the output to a wave file.
# Corrected version.

import pyaudio, wave, struct, math
import numpy as np
from scipy.signal import butter, lfilter

import matplotlib.pyplot as plt

import scipy


wavfile = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/midterm/testingjinchenglatest.wav'
output_wavfile = 'author_output_blocks_corrected.wav'

print('Play the wave file %s.' % wavfile)

# Open wave file (should be mono channel)
wf = wave.open( wavfile, 'rb' )

# Read the wave file properties
CHANNELS        = wf.getnchannels()     # Number of channels
RATE            = wf.getframerate()     # Sampling rate (frames/second)
signal_length   = wf.getnframes()       # Signal length
WIDTH           = wf.getsampwidth()     # Number of bytes per sample
fs = 1600
print('The file has %d channel(s).'            % CHANNELS)
print('The frame rate is %d frames/second.'    % RATE)
print('The file has %d frames.'                % signal_length)
print('There are %d bytes per sample.'         % WIDTH)

output_wf = wave.open(output_wavfile, 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)

# Difference equation coefficients
b0 =  0.008442692929081
b2 = -0.016885385858161
b4 =  0.008442692929081
b = [b0, 0.0, b2, 0.0, b4]

# a0 =  1.000000000000000
a1 = -3.580673542760982
a2 =  4.942669993770672
a3 = -3.114402101627517
a4 =  0.757546944478829
a = [1.0, a1, a2, a3, a4]

from matplotlib import pyplot
BLOCKLEN = 1024
pyplot.ion()           # Turn on interactive mode
pyplot.figure(1)
[g1] = pyplot.plot([], [], 'blue', label='input signal')
[g2] = pyplot.plot([], [], 'green', label='output signal')
[g3] = pyplot.plot([], [], 'black', label='fft')

n = range(0, BLOCKLEN)
pyplot.xlim(0, BLOCKLEN)         # set x-axis limits
pyplot.xlabel('Time (n)')
g1.set_xdata(n)      
g2.set_xdata(n)              # x-data of plot (discrete-time)
g3.set_xdata(n)
pyplot.ylim(-10000, 10000)        # set y-axis limits
pyplot.legend()








p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = False,
    output      = True )


MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Get first set of frame from wave file
binary_data = wf.readframes(BLOCKLEN)






ORDER = 4   # filter is fourth order
states = np.zeros(ORDER)

while len(binary_data) == WIDTH * BLOCKLEN:
    

    # convert binary data to numbers
    input_block = struct.unpack('h' * BLOCKLEN, binary_data) 


    b, a = scipy.signal.butter(2, [0.075, 0.725], 'bandstop') 
    [output_block, states] = scipy.signal.lfilter(b, a, input_block, zi = states)


    X1 = np.fft.fft(input_block)
    X2 = np.fft.fft(output_block)
    


    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)

    # convert to integer
    output_block = output_block.astype(int)

    # Convert output value to binary data
    binary_data = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio stream
    stream.write(binary_data)


# Update y-data of plot
    g3.set_ydata(X2)


    g1.set_ydata(input_block)   # Update y-data of plot
    g2.set_ydata(output_block)   # Update y-data of plot
    pyplot.pause(0.00001)
    

    # Write binary data to output wave file
    output_wf.writeframes(binary_data)

    # Get next frame from wave file
    binary_data = wf.readframes(BLOCKLEN)

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()

# Close wavefiles
wf.close()
output_wf.close()