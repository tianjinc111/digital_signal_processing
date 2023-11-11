import pyaudio
import struct
import pyautogui  # to press a button to play the game

# below are the four wake word's path that you have generated earlier
from pvporcupine import Porcupine
key1 = r'/Users/jinchengbaby/Desktop/python-sokoban-master/voice/go-to-down_en_windows_v2_1_0.ppn'
key2 =r'/Users/jinchengbaby/Desktop/python-sokoban-master/voice/go-to-up_en_windows_v2_1_0.ppn'
key3 = r'/Users/jinchengbaby/Desktop/python-sokoban-master/voice/go-to-right_en_windows_v2_1_0.ppn'
key4 = r'/Users/jinchengbaby/Desktop/python-sokoban-master/voice/go-to-left_en_windows_v2_1_0.ppn'

# this is the library path that you can fnd inside Porcupine -> lib -> system(windows or linux or mac) -> os type( 64 or 32 bit)
library_path = r'/opt/anaconda3/envs/pyaudio2/lib/python3.6/site-packages/pvporcupine/lib/mac/arm64/libpv_porcupine.dylib'
# this is model file path can be find inside Porcupine -> lib -> common
model_file_path = r'/opt/anaconda3/envs/pyaudio2/lib/python3.6/site-packages/pvporcupine/lib/common/porcupine_params.pv'
keyword_file_paths = [key1, key2, key3, key4]
sensitivities = [0.5, 0.5, 0.5, 0.5]
handle = Porcupine('M8pei9cpUCyZUCni1XCjXuWDEXIdP3pwGnwRhbU2nMQVD/iYc73TAw==', library_path, model_file_path,
                   keyword_paths=keyword_file_paths, sensitivities=sensitivities)


def get_next_audio_frame():
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=handle.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                           frames_per_buffer=handle.frame_length, input_device_index=None)
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    return pcm


def listen_for_keyword():
    while True:
        pcm = get_next_audio_frame()
        keyword_index = handle.process(pcm)
        # print(keyword_index)
        if keyword_index == 1:
            print(keyword_index)
            pyautogui.press('up')
        if keyword_index == 3:
            print(keyword_index)
            pyautogui.press('left')
        if keyword_index == 2:
            print(keyword_index)
            pyautogui.press('right')
        if keyword_index == 0:
            print(keyword_index)
            pyautogui.press('down')
