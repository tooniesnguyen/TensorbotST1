import speech_recognition as sr
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Listening...")
    audio = recognizer.listen(source)
try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, I could not understand.")