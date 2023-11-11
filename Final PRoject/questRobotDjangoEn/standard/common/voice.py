import speech_recognition as sr



def reg(obj):
    r = sr.Recognizer()  # init
    test = sr.AudioFile(obj)  # wav file
    with test as source:
        audio = r.record(source)
    # type(audio)
    c = r.recognize_google(audio, language='zh-cn')  # result output
    print(c)
    return c
