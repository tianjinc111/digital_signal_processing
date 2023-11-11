import pyaudio
import struct
import math
import wave
import tkinter as Tk
from myfunctions import clip16


def fun_start():
    wavfile_input = "/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/testing zgm/Q1.wav"
    wf_input = wave.open(wavfile_input, 'rb')

    # Read wave file properties
    RATE = wf_input.getframerate()  # Frame rate (frames/second)
    WIDTH = wf_input.getsampwidth()  # Number of bytes per sample
    LEN = wf_input.getnframes()  # Signal length
    CHANNELS = wf_input.getnchannels()  # Number of channels

    print('The input file has %d channel(s).' % CHANNELS)
    print('The input file has %d frames/second.' % RATE)
    print('The input file has %d frames.' % LEN)
    print('The input file has %d bytes per sample.' % WIDTH)

    wavfile_output = 'output_Q1.wav'
    wf_output = wave.open(wavfile_output, 'w')
    wf_output.setframerate(RATE)  # Sampling rate (frames/second)
    wf_output.setnchannels(CHANNELS)  # Number of channels
    wf_output.setsampwidth(WIDTH)  # Number of bytes per sample

    print('The output file is %s.' % wavfile_output)

    delay_sec = 0.05  # delay in seconds, 50 milliseconds
    N = int(RATE * delay_sec)  # delay in samples

    # Buffer to store past signal values. Initialize to zero.
    BUFFER_LEN = N  # length of buffer
    buffer = BUFFER_LEN * [0]  # list of zeros

    # Buffer indices
    kr = 0  # read index
    kw = int(0.5 * BUFFER_LEN)  # write index

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=False, output=True, frames_per_buffer=128)

    print('* Start')

    for N in range(0, LEN):
        # root.update()

        # Get sample from wave file
        input_bytes = wf_input.readframes(1)

        # Convert string to number
        x0, = struct.unpack('h', input_bytes)

        # Get previous and next buffer values (since kr is fractional)
        kr_prev = int(math.floor(kr))
        frac = kr - kr_prev  # 0 <= frac < 1
        kr_next = kr_prev + 1
        if kr_next == BUFFER_LEN:
            kr_next = 0

        # Compute output value using interpolation
        y0 = x0 + gain.get() * ((1 - frac) * buffer[kr_prev] + frac * buffer[kr_next])

        # Update buffer
        buffer[kw] = x0

        # Increment read index
        kr = kr + 1 + lfo_sd.get() * math.sin(2 * math.pi * lfo_freq.get() * N / RATE)
        # Note: kr is fractional (not integer!)

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

        # Write output to output wave file
        wf_output.writeframes(output_bytes)

    print('* Finished')

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf_input.close()
    wf_output.close()


if __name__ == "__main__":
    # Define Tkinter root
    root = Tk.Tk()

    # Define title
    root.title('Chorus Effect')

    # Define Tk variables
    gain = Tk.DoubleVar()
    lfo_freq = Tk.DoubleVar()
    lfo_sd = Tk.DoubleVar()

    # Initialize Tk variables
    gain.set(1)
    lfo_freq.set(2)
    lfo_sd.set(0)

    # Define widgets
    S_gain = Tk.Scale(root, label='Gain', variable=gain, from_=0, to=2**15 - 1, tickinterval=1)
    S_lfo_freq = Tk.Scale(root, label='LFO frequency', variable=lfo_freq, from_=0, to=20, tickinterval=1)
    S_lfo_sd = Tk.Scale(root, label='LFO sweep depth', variable=lfo_sd, from_=0, to=1, tickinterval=0.1)
    B_start = Tk.Button(root, text='Start', command=fun_start)
    B_quit = Tk.Button(root, text='Quit', command=lambda: root.destroy())

    # Place widgets
    B_quit.pack(side=Tk.BOTTOM, fill=Tk.X)
    B_start.pack(side=Tk.BOTTOM, fill=Tk.X)
    S_gain.pack(side=Tk.LEFT)
    S_lfo_freq.pack(side=Tk.LEFT)
    S_lfo_sd.pack(side=Tk.LEFT)

    root.mainloop()
