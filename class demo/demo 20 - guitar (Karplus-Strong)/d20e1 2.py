## implemented based on the echo-via circulatr buffer.py 


import pyaudio

import struct

import numpy as np
import random


# Signal information
RATE     = 8000
WIDTH    = 2
CHANNELS = 1

duration = 2 

MAXVALUE = 2**15-1  


def clip16( x ):    
    # Clipping for 16 bits
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    else:
        x = x        
    return (x)



def filterfunction(k, output_value):

    output_value -= (a[N] * buffer[(k+ 1) % N] + a[N + 1] * buffer[k % N])
    
    return output_value




# Karplus-Strong paramters
K = 0.93
N = 60
b = 1
a = [0] * (N + 2)
a[0] = 1
a[-1] = -K/2
a[-2] = -K/2




x = [0] * N
for i in range (N):
    x[i] = random.random() * 10000
for _ in range(duration * RATE):
    x.append(0)


# Create a buffer to store past values. Initialize to zero.
BUFFER_LEN = N + 1   # N+1 is kept because we want max delay of N+1 samples
buffer = [ 0 for i in range(BUFFER_LEN) ]    


p = pyaudio.PyAudio()

PA_FORMAT = p.get_format_from_width(WIDTH)

stream = p.open(
    format      = p.get_format_from_width(WIDTH),
    channels    = CHANNELS,
    rate        = RATE,
    input       = False,
    output      = True )

k = 0       


print("Started...")


i = 0
while i < (len(x)):

    # Convert string to number
    input_value = x[i]

    output_value = b * input_value
    
    output_value = filterfunction(k,output_value)
   
    # Update buffer
    buffer[k] = output_value

    # Increment buffer index
    k = k + 1
    if k >= BUFFER_LEN:
        # The index has reached the end of the buffer. Circle the index back to the front.
        k = 0

    output_bytes = struct.pack('h', int(clip16(output_value)))


    stream.write(output_bytes)    

    i += 1

    #output_wf.writeframes(output_string)

print("...Finished")

stream.stop_stream()
stream.close()
#
p.terminate()