# echo_via_circular_buffer.py
# Reads a specified wave file (mono) and plays it with an echo.
# This implementation uses a circular buffer.

import pyaudio
import wave
import struct
import numpy as np
from myfunctions import clip16

WIDTH = 2
CHANNELS = 1
RATE = 8000
DURATION = 2

K = 0.93
N = 60

gain = 10000

x = [gain * np.random.randn() for i in range(N)] + [0] * round(DURATION * RATE)

# Create a buffer to store past values. Initialize to zero.
BUFFER_LEN = N  # length of buffer
buffer = BUFFER_LEN * [0]   # list of zeros

# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True)

# Initialize buffer index (circular index)
k = 0

print("Started...")

for i in range(DURATION * RATE + N):

    # Compute output value
    output_value = x[i] - buffer[(k + 1) % BUFFER_LEN] * (-K/2) - buffer[k] * (-K/2)

    # Update buffer
    buffer[k] = output_value

    # Increment buffer index
    k = k + 1
    if k >= BUFFER_LEN:
        # The index has reached the end of the buffer. Circle the index back to the front.
        k = 0

    # Clip and convert output value to binary data
    output_bytes = struct.pack('h', int(clip16(output_value)))

    # Write output value to audio stream
    stream.write(output_bytes)


print("...Finished")

stream.stop_stream()
stream.close()
p.terminate()
