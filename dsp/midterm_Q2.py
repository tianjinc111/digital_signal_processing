import pyaudio
import struct
import wave
import numpy as np
from myfunctions import clip16
import scipy.signal
import scipy.fftpack

wavfile_input = "/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/dsp/kengmingchang.wav"
wf_input = wave.open(wavfile_input, 'rb')

# Read wave file properties
RATE = wf_input.getframerate()  # Frame rate (frames/second)
WIDTH = wf_input.getsampwidth()  # Number of bytes per sample
LEN = wf_input.getnframes()  # Signal length
CHANNELS = wf_input.getnchannels()  # Number of channels

print('The file has %d channel(s).' % CHANNELS)
print('The file has %d frames/second.' % RATE)
print('The file has %d frames.' % LEN)
print('The file has %d bytes per sample.' % WIDTH)

wavfile_output = 'output_Q2_my_talking.wav'
wf_output = wave.open(wavfile_output, 'w')
wf_output.setframerate(RATE)  # Sampling rate (frames/second)
wf_output.setnchannels(CHANNELS)  # Number of channels
wf_output.setsampwidth(WIDTH)  # Number of bytes per sample

print('The output wave file is %s.' % wavfile_output)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=False, output=True)

BLOCKLEN = 2**15
MAXVALUE = 2**15 - 1  # Maximum allowed output signal value (because WIDTH = 2)


# Get first set of frame from wave file
binary_data = wf_input.readframes(BLOCKLEN)

while len(binary_data) == WIDTH * BLOCKLEN:

    # convert binary data to numbers
    input_block = struct.unpack('h' * BLOCKLEN, binary_data)

    b, a = scipy.signal.butter(N=4, Wn=[0.1, 0.5], btype='bandstop') # for bandpass and bandstop filters, Wn is a length-2 sequence.
    output_block, _ = scipy.signal.lfilter(b, a, input_block, zi=np.zeros(8))

    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)

    # convert to integer
    output_block = output_block.astype(int)

    # Convert output value to binary data
    binary_data = struct.pack('h' * BLOCKLEN, *output_block)

    # Write binary data to audio stream
    stream.write(binary_data)

    # Write binary data to output wave file
    wf_output.writeframes(binary_data)

    # Get next frame from wave file
    binary_data = wf_input.readframes(BLOCKLEN)

stream.stop_stream()
stream.close()
p.terminate()
wf_input.close()
wf_output.close()
