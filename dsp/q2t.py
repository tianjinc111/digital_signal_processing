import pyaudio, struct
import wave, math
import numpy as np
import scipy.signal
from scipy.signal import butter, lfilter
from math import cos, pi 
import scipy.io.wavfile as wf

wavfile = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/midterm/testingjinchenglatest.wav'



output_wavfile = 'q2t.wav'

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

K = 4

#low pass


def butter_bandstop(lowcut, highcut, fs, order=2):
    print(fs)
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    print(nyq, lowcut, highcut)
    print(low, high)
    b, a = butter(order, [low, high], 'bandstop')
    
    return b, a

# bandpass filter
def bandstop_filter(data, center, fs, states, order=2):
    # generate lowcut and highcut
    lowcut = center - 1300
    highcut = center + 1300
    # generate a, b
    b, a = butter_bandstop(lowcut, highcut, fs, order=order)
    [y, states] = lfilter(b, a, data, zi=states)
    # normalize the output
    y = np.clip(y, -MAXVALUE, MAXVALUE)
    # transform the type of output to int
    y = y.astype(int)
    return [y, states]

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = False,
    output      = True )

BLOCKLEN = 1024
MAXVALUE = 2**15-1  # Maximum allowed output signal value (because WIDTH = 2)

# Get first set of frame from wave file
binary_data = wf.readframes(BLOCKLEN)
# filter is fourth order
states = np.zeros(K)

while len(binary_data) == WIDTH * BLOCKLEN:

    # convert binary data to numbers
    input_block = struct.unpack('h' * BLOCKLEN, binary_data) 

    # filter
    [output_block, states] = bandstop_filter(input_block, fs, RATE, states)

    # convert to integer
    output_block = output_block.astype(int)

    # Convert output value to binary data
    binary_data = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio stream
    stream.write(binary_data)

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