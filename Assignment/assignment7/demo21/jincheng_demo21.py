### demo 21


import pyaudio
import struct
import wave
import numpy as np
from pyparsing import java_style_comment
from scipy import signal
from math import pi, exp



print('Started...')

fs = 16000          # Sampling frequency
CHANNELS = 1        # Mono channel
DURATION = 10       # 10 seconds to take input from mic
fr = 8              # Frame rate
N = fs * DURATION   # N total sample number for the specified duration
K = 7           # Complex filter


[b_lpf, a_lpf] = signal.ellip(K, 0.2, 50, 0.48)



# Define imaginary coefficients
I = 1j

# % s = exp( I * 0.5 * pi * (0:K) );   
# s = I.^(0:K);         % (equivalent)


s = [I ** i for i in range(K + 1)]
a = [0 * l for l in range(0, K + 1)]
b = [0 * l for l in range(0, K + 1)]


for k in range(0, K + 1):
    b[k] = b_lpf[k] * s[k]
    a[k] = a_lpf[k] * s[k]

s = np.array(s)
b_lpf = np.array(b_lpf)
a_lpf = np.array(a_lpf)
a = a_lpf * s
b = b_lpf * s

a = list(a)

b = list(b)


# Pyaudio object
p = pyaudio.PyAudio()


WIDTH    = 2



stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = fs,
    input       = True,
    output      = True )


n = [i for i in range(fr)]

n = np.array(n)

t = n / fs



for k in range(0, int(N / fr)):
    # Read from the microphone, real-time
    string = stream.read(fr, exception_on_overflow=False)
    input_block = struct.unpack('h' * fr, string)

    output_block = signal.lfilter(b, a, input_block)

    
    f1 = 400

    # g = [1j for i in range(K + 1)]
    c = np.e ** (I * 2 * pi * f1 * (t / fs)) 

    
    g = np.real(output_block * c)
    y = [0 for i in range(fr)]


    for i in range(0, fr):

        y[i] = int(g[i])
        output = struct.pack('h', y[i])

        stream.write(output)




    

# close the wave file, stop the audio stream to headphones
print("...Done")

stream.stop_stream()
stream.close()
p.terminate()