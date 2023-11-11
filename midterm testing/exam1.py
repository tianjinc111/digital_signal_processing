# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
import math
import pyaudio
import struct
import wave


# %%
# myfunctions: Clipping for 16 bits
def clip16(x):
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    return (x)

# %% [markdown]
# # Q1. Chorus effect with GUI

# %%
input_wf = wave.open('/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/testing zgm/Q1.wav', 'rb')
# Read wave file properties
RATE = input_wf.getframerate()
WIDTH = input_wf.getsampwidth()
LEN = input_wf.getnframes()
CHANNELS = input_wf.getnchannels()
print(f"rate: {RATE}, width: {WIDTH}, len: {LEN}, ch: {CHANNELS}")
output_wf = wave.open('output_Q1.wav', 'w')
output_wf.setnchannels(CHANNELS)
output_wf.setsampwidth(WIDTH)
output_wf.setframerate(RATE)


# %%
# Buffer
BUFFER_LEN = int(RATE * 0.03)
buffer = BUFFER_LEN * [0]  # initialize to zero
# Buffer indices
kr = 0  # read index
kw = int(0.5 * BUFFER_LEN)  # write index
print(f"buffer len: {BUFFER_LEN}")


# %%
# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True)
# Coefficients
g = 0.8  # gain
f0 = 2  # LFO frequency
W = 0.2  # LFO sweep depth
# Process
y = []


CONTINUE = True
for n in range(0, LEN):
    if not CONTINUE:
        break

    input_bytes = input_wf.readframes(1)  # get sample from wav
    x0, = struct.unpack('h', input_bytes)  # Convert string to number
    # Get buffer values
    kr_prev = int(math.floor(kr))
    frac = kr - kr_prev  # 0 <= frac < 1
    kr_next = kr_prev + 1
    if kr_next == BUFFER_LEN:
        kr_next = 0
    # Compute output value using interpolation
    y0 = x0 + g * ((1 - frac) * buffer[kr_prev] + frac * buffer[kr_next])  # 2.29
    y.append(y0)
    # Update buffer
    buffer[kw] = x0
    # Increment read index
    kr = kr + 1 + W * math.sin(2 * math.pi * f0 * n / RATE)  # 2.34
    # Ensure that 0 <= kr < BUFFER_LEN
    if kr >= BUFFER_LEN:
        # End of buffer. Circle back to front.
        kr = kr - BUFFER_LEN
    # Increment write index
    kw = kw + 1
    if kw == BUFFER_LEN:
        # End of buffer. Circle back to front.
        kw = 0
    # Clip and convert output value to binary data
    output_bytes = struct.pack('h', int(clip16(y0)))
    # Write output to audio stream
    stream.write(output_bytes)


# %%
# save output signal
for n in range(0, LEN):
    output_bytes = struct.pack('h', int(clip16(y[n])))
    output_wf.writeframes(output_bytes)
stream.stop_stream()
stream.close()
p.terminate()
output_wf.close()


# %%



