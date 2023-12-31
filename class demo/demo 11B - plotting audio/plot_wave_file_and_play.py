# plot_wave_file_and_play.py

import pyaudio
import struct
import wave
from matplotlib import pyplot

# Specify wave file
wavfile = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/midterm/audio_Q2.wav'
print('Name of wave file: %s' % wavfile)

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

BLOCKLEN = 1000    # Blocksize

# Set up plotting...

pyplot.ion()           # Turn on interactive mode so plot gets updated

fig = pyplot.figure(1)

[g1] = pyplot.plot([], [])

g1.set_xdata(range(BLOCKLEN))
pyplot.ylim(-32000, 32000)
pyplot.xlim(0, BLOCKLEN)

# Open the audio output stream
p = pyaudio.PyAudio()

PA_FORMAT = p.get_format_from_width(WIDTH)
stream = p.open(
    format = PA_FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = False,
    output = True,
    frames_per_buffer = 256)      # low latency so that plot and output audio are synchronized

# Get block of samples from wave file
input_bytes = wf.readframes(BLOCKLEN)

while len(input_bytes) >= BLOCKLEN * WIDTH:

    # Convert binary data to number sequence (tuple)
    signal_block = struct.unpack('h' * BLOCKLEN, input_bytes)

    g1.set_ydata(signal_block)
    pyplot.pause(0.0001)

    # Write binary data to audio output stream
    stream.write(input_bytes, BLOCKLEN)

    # Get block of samples from wave file
    input_bytes = wf.readframes(BLOCKLEN)

stream.stop_stream()
stream.close()
p.terminate()

wf.close()

pyplot.ioff()           # Turn off interactive mode
pyplot.show()           # Keep plot showing at end of program
pyplot.close()
print('* Finished')
