
import wave

eight_bit_file_name = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/testing1_8bit.wav'

wf = wave.open(eight_bit_file_name)

print('file name:', eight_bit_file_name ) 

print('number of bytes per eight bits sample:', wf.getsampwidth() )


#here are the code for printing the sample width for 32 bit formats

thirtytwo_bit_file_name = '/Users/jinchengbaby/Desktop/jincheng Tian tandon second semester/dsp/testing1_32bit.wav'

wf = wave.open(thirtytwo_bit_file_name)

print('file name:', thirtytwo_bit_file_name ) 

print('number of bytes per eight bits sample:', wf.getsampwidth() )


print(wf.getframerate())