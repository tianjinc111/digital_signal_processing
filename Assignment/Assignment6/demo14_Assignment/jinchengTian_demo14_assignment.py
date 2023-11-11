# demo_filter_blocks_corrected.py
# Block filtering of a wave file, save the output to a wave file.
# Corrected version.

from cProfile import label
import pyaudio, wave, struct, math
import numpy as np
import scipy.signal


from myfunctions import clip16

from matplotlib import pyplot


#wavfile = 'author.wav'

# wavfile = "demo 14 - block filtering/author.wav"
output_wavfile = 'jincheng_mic_output_blocks_corrected.wav'

#print('Play the wave file %s.' % wavfile)

# Open wave file (should be mono channel)
# wf = wave.open( wavfile, 'rb' )

# Read the wave file properties

# CHANNELS        = wf.getnchannels()     # Number of channels
# RATE            = wf.getframerate()     # Sampling rate (frames/second)
# signal_length   = wf.getnframes()       # Signal length
# WIDTH           = wf.getsampwidth()     # Number of bytes per sample





WIDTH       = 2         # Number of bytes per sample
CHANNELS    = 1         # mono
RATE        = 16000     # Sampling rate (frames/second)
DURATION    = 15     # duration of processing (seconds)




N = DURATION * RATE     # N : Number of samples to process

print('The file has %d channel(s).'            % CHANNELS)
print('The frame rate is %d frames/second.'    % RATE)
print('There are %d bytes per sample.'         % WIDTH)

output_wf = wave.open(output_wavfile, 'w')      # wave file
output_wf.setframerate(RATE)
output_wf.setsampwidth(WIDTH)
output_wf.setnchannels(CHANNELS)





pyplot.ylim(-10000,10000)        # set y-axis limits



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

p = pyaudio.PyAudio()




PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(
    format = PA_FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    output = True,
    frames_per_buffer = 256)   




BLOCKLEN = 2 **10
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

pyplot.ion()           # Turn on interactive mode
pyplot.figure(1)




[g1] = pyplot.plot([],[], 'blue', label = 'input')
[g2] = pyplot.plot([],[], 'red', label = 'ouput')






n = range(0, BLOCKLEN)
pyplot.xlim(0, BLOCKLEN)         # set x-axis limits
pyplot.xlabel('Time (n)')
g1.set_xdata(n)                   # x-data of plot (discrete-time)
g2.set_xdata(n)                   # x-data of plot (discrete-time)
pyplot.legend()








DBscale = False


# Initialize plot window:
pyplot.figure(2)
if DBscale:
    pyplot.ylim(0, 150)
else:
    pyplot.ylim(0, 20*RATE)

# Frequency axis (Hz)
pyplot.xlim(0, 0.5*RATE)         # set x-axis limits
# plt.xlim(0, 2000)         # set x-axis limits
pyplot.xlabel('Frequency (Hz)')
f = RATE/BLOCKLEN * np.arange(0, BLOCKLEN)

line, = pyplot.plot([], [], color = 'blue', label = "input")  # Create empty line

line2, = pyplot.plot([], [], color = 'black', label = "output")
line.set_xdata(f)     
line2.set_xdata(f)                    # x-data of plot (frequency)
pyplot.legend()


# Get first set of frame from wave file
#
# binary_data = wf.readframes(BLOCKLEN)

ORDER = 4   # filter is fourth order
states = np.zeros(ORDER)



K = int( DURATION * RATE / BLOCKLEN )   # Number of blocks

for i in range(K):

    # convert binary data to numbers
    #input_block = struct.unpack('h' * BLOCKLEN, binary_data) 

    input_bytes = stream.read(BLOCKLEN, exception_on_overflow = False)

    input_block = struct.unpack('h' * BLOCKLEN, input_bytes)

    # filter
    [output_block, states] = scipy.signal.lfilter(b, a, input_block, zi = states)

    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)


    # convert to integer
    output_block = output_block.astype(int)


    



    X = np.fft.fft(input_block)
    Y = np.fft.fft(output_block)


     # Update y-data of plot
    if DBscale:
        line.set_ydata(20 * np.log10(np.abs(X)))
        line2.set_ydata(20 * np.log10(np.abs(Y)))

    else:
        line.set_ydata(np.abs(X))
        line2.set_ydata(np.abs(Y))
    pyplot.pause(0.001)




    # plt.draw()
    g1.set_ydata(input_block)   # Update y-data of plot
    g2.set_ydata(output_block)   # Update y-data of plot
    pyplot.pause(0.00001)

    # Convert output value to binary data
    input_block = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio stream
    stream.write(input_bytes)

    # Write binary data to output wave file
    output_wf.writeframes(input_bytes)

    # Get next frame from wave file
    

print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()

# Close wavefiles
#
output_wf.close()