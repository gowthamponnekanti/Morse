import speech_recognition as sr
print('speak now !!!')
r = sr.Recognizer()
with sr.Microphone() as source:
    audio = r.listen(source)
try:
    print(r.recognize_google(audio))
except Exception:
    print("Something went wrong !!")
