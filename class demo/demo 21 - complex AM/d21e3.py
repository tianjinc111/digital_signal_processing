import pyaudio
import struct
import numpy as np
from scipy import signal
from math import pi


WIDTH = 2
CHANNELS = 1  # Mono channel
DURATION = 10  # 10 seconds to take input from mic
BLOCKLEN = 8  # Frame rate

fs = 16000  # Sampling frequency
f1 = 400
N = fs * DURATION  # N total sample number for the specified duration
K = 7  # Complex filter

[b_lpf, a_lpf] = signal.ellip(K, 0.2, 50, 0.48)

# complex modulate filter coefficients to get complex filter
I = 1j
s = [I**i for i in range(K + 1)]
b = [b_lpf[i] * s[i] for i in range(K + 1)]
a = [a_lpf[i] * s[i] for i in range(K + 1)]
n = np.array([i for i in range(BLOCKLEN)])
t = n / fs

# Pyaudio object
p = pyaudio.PyAudio()
# Open a stream to read and write audio
stream = p.open(rate=fs,
                channels=CHANNELS,
                format=p.get_format_from_width(WIDTH),
                input=True,
                output=True)

print('Started...')

for _ in range(int(N / BLOCKLEN)):
    # Get frames from audio input stream
    # input_bytes = stream.read(BLOCKLEN)       # BLOCKLEN = number of frames read
    input_bytes = stream.read(BLOCKLEN, exception_on_overflow=False)  # BLOCKLEN = number of frames read

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h' * BLOCKLEN, input_bytes)

    # Apply filter on the read data
    output_block = signal.lfilter(b, a, input_tuple)

    # Combination of real and I part
    g = np.real(output_block * np.e**(I * 2 * pi * f1 * (t / fs)))
    y = map(int, g)

    output = struct.pack('h' * BLOCKLEN, *y)
    stream.write(output)

# close the wave file, stop the audio stream to headphones
print("...Done")
stream.stop_stream()
stream.close()
p.terminate()
