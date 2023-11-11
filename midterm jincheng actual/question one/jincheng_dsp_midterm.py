
# %%
import math
import pyaudio
import struct
import wave
import tkinter as Tk



def quit():
    global CONTINUE
    print('Good bye')
    CONTINUE = False
    
    
# myfunctions: Clipping for 16 bits
def clip16(x):
    if x > 32767:
        x = 32767
    elif x < -32768:
        x = -32768
    return (x)




inputwave = wave.open('audio_Q1.wav', 'rb')
# Read wave file properties
RATE = inputwave.getframerate()
WIDTH = inputwave.getsampwidth()
LEN = inputwave.getnframes()
CHANNELS = inputwave.getnchannels()
print(f"rate: {RATE}, width: {WIDTH}, len: {LEN}, ch: {CHANNELS}")
outputwave = wave.open('output_Q1.wav', 'w')
outputwave.setnchannels(CHANNELS)
outputwave.setsampwidth(WIDTH)
outputwave.setframerate(RATE)



# Buffer
delay_sec = 1
BUFFER_LEN = int(RATE * delay_sec)
buffer = BUFFER_LEN * [0]  # initialize to zero
kr = 0  # read index
kw = int(0.1 * BUFFER_LEN)  # write index



# Coefficient
# Define Tkinter root
root = Tk.Tk()

gain = Tk.DoubleVar()  # gain
frequency = Tk.DoubleVar()  # LFO frequency
depth = Tk.DoubleVar()  # LFO sweep depth
# Initialize Tk variables
gain.set(1.0)   # f1 : frequency of sinusoid (Hz)
frequency.set(2)
depth.set(5)
# Define widgets
S_gain = Tk.Scale(root, label='Gain', variable=gain, from_=0, to=10, resolution=0.1)
S_f0 = Tk.Scale(root, label='LFO frequency(Hz)', variable=frequency, from_=0, to=10000, resolution=1)
S_w = Tk.Scale(root, label='LFO sweep depth(ms)', variable=depth, from_=5, to=10000, resolution=1)
B_quit = Tk.Button(root, text='Quit', command=quit)

# Place widgets
B_quit.pack(side=Tk.BOTTOM, fill=Tk.X)
S_gain.pack(side=Tk.LEFT)
S_f0.pack(side=Tk.LEFT)
S_w.pack(side=Tk.LEFT)


# %%
# Open an output audio stream
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=False,
                output=True,
                frames_per_buffer=BUFFER_LEN)




CONTINUE = True


for n in range(0, LEN):
    if not CONTINUE:
        break
    
    root.update()
    input_bytes = inputwave.readframes(1)  
    if not input_bytes:
        break
    x0, = struct.unpack('h', input_bytes)  

    kr_prev = int(math.floor(kr))
    
    # print(f0.get())
    
    
    kr_prev_2 = int(math.floor(kr) + 5)
    frac = kr - kr_prev  
    frac_2 = kr - kr_prev_2
    kr_next = kr_prev + 1
    
    kr_next_2 = kr_next + 10
    if kr_next >= BUFFER_LEN:
        kr_next = 0
        
    if kr_next_2 >= BUFFER_LEN:
        kr_next_2 = 0
    # Compute output value using interpolation
    y0 = x0 + gain.get() * ((1 - frac) * buffer[kr_prev] + frac * buffer[kr_next] + frac_2 * buffer[kr_next_2])  # 2.29
   
    # Update buffer
    buffer[kw] = x0
    # Increment read index
    kr = kr + 1 + depth.get() / 1000 * math.sin(2 * math.pi * frequency.get() * n / RATE)  # 2.34
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
    outputwave.writeframes(output_bytes)



stream.stop_stream()
stream.close()
p.terminate()
outputwave.close()

