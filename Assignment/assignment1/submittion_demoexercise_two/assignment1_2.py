
import wave

file_name = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/testing1_16bit.wav'

wf = wave.open(file_name)

print('file name:', file_name ) 
print('number of channels:', wf.getnchannels() ) 
print('number of frames per second:', wf.getframerate() )
print('signal length:', wf.getnframes() )
print('number of bytes per sample:', wf.getsampwidth() )

wf.close()

