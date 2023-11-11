# mic_filter.py
# Record from microphone, filter the signal,
# and play the output signal on the loud speaker.

import pyaudio
import struct
from math import cos, pi
import wave

from myfunctions import clip16

WIDTH       = 2         # Number of bytes per sample
CHANNELS    = 1         # mono
RATE        = 16000     # Sampling rate (frames/second)
DURATION    = 6         # duration of processing (seconds)

N = DURATION * RATE     # N : Number of samples to process

f0 = 400 # Hz

my_talking = wave.open("my_talking4.wav", "w")
my_talking.setnchannels(CHANNELS)
my_talking.setsampwidth(WIDTH)
my_talking.setframerate(RATE)

p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = True,
    output      = True)

print('* Start')

for n in range(0, N):

    # Get one frame from audio input (microphone)
    input_bytes = stream.read(1)
    # If you get run-time time input overflow errors, try:
    # input_bytes = stream.read(1, exception_on_overflow = False)

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h', input_bytes)

    # Convert one-element tuple to number
    x = input_tuple[0]

    # Difference equation
    y = x * cos(2 * pi * f0 * n)

    # Compute output value
    output_value = int(clip16(y))    # Number

    # Convert output value to binary data
    output_bytes = struct.pack('h', output_value)  

    # Write binary data to audio stream
    stream.write(output_bytes)

    my_talking.writeframesraw(output_bytes)


print('* Finished')

my_talking.close()

stream.stop_stream()
stream.close()
p.terminate()
