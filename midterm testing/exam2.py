# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
import math
import pyaudio
import struct
import wave
import numpy as np
from scipy import fft, fftpack, signal
from matplotlib import pyplot as plt


# %%
# myfunctions: Clipping for 16 bits
def clip16(x):
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    return (x)

# %% [markdown]
# # Q2. Tonal noise suppression

# %%
input_wf = wave.open('/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/midterm/audio_Q2.wav', 'rb')
# Read wave file properties
RATE = input_wf.getframerate()
WIDTH = input_wf.getsampwidth()
LEN = input_wf.getnframes()
CHANNELS = input_wf.getnchannels()
print(f"rate: {RATE}, width: {WIDTH}, len: {LEN}, ch: {CHANNELS}")
output_wf = wave.open('output_Q2.wav', 'w')
output_wf.setnchannels(CHANNELS)
output_wf.setsampwidth(WIDTH)
output_wf.setframerate(RATE)


# %%
# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True)

BLOCKLEN = 64  # Block len
MAXVALUE = 2**15 - 1  # Maximum allowed output signal value (because WIDTH = 2)
gpass, gstop = 1, 40  # iirdesign
bw = 4000  # bandwidth

# Get first set of frame from wave file
binary_data = input_wf.readframes(BLOCKLEN)
while len(binary_data) == WIDTH * BLOCKLEN:
    # convert binary data to numbers
    input_block = struct.unpack('h' * BLOCKLEN, binary_data)
    # peak filter
    sig_fft = fftpack.fft(input_block)
    power = np.abs(sig_fft)**2
    sample_freq = fftpack.fftfreq(BLOCKLEN, d=1 / RATE)
    pos_mask = np.where(sample_freq > 0)
    freqs = sample_freq[pos_mask]
    peak_freq = freqs[power[pos_mask].argmax()]
    # if peak_freq:
    ws = np.array([peak_freq - bw / 2, peak_freq + bw / 2]) / RATE * 2
    wp = [max(0, ws[0] - 0.1), min(ws[1] + 0.1, 1)]
    if ws[0] <= wp[0]:
        ws, wp = ws[1], wp[1]
    elif ws[1] >= wp[1]:
        ws, wp = ws[0], wp[0]
    # b, a = signal.iirdesign(wp, ws, gpass, gstop, fs=RATE)  # Bandstop
    b, a = signal.iirdesign(3500, peak_freq, gpass, gstop, fs=RATE)  # Bandstop
    output_block = 10000 * signal.filtfilt(b, a, input_block)

    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)
    # convert to integer
    output_block = output_block.astype(int)
    # Convert output value to binary data
    binary_data = struct.pack('h' * BLOCKLEN, *output_block)
    # Write binary data to audio stream
    stream.write(binary_data)
    # Write binary data to output wave file
    output_wf.writeframes(binary_data)
    # Get next frame from wave file
    binary_data = input_wf.readframes(BLOCKLEN)

    plt.plot(input_block)
    plt.plot(output_block)


# %%
plt.plot(input_block)
plt.plot(output_block)


# %%
stream.stop_stream()
stream.close()
p.terminate()
# Close wavefiles
input_wf.close()
output_wf.close()


# %%



