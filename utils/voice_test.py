import speech_recognition as sr

for mic in sr.Microphone.list_microphone_names():
    print(mic)