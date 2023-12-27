import speech_recognition as sr
<<<<<<< Updated upstream

for mic in sr.Microphone.list_microphone_names():
    print(mic)
=======
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source, timeout = 5, phrase_time_limit=5)
try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand.")
>>>>>>> Stashed changes
