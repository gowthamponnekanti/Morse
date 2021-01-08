import speech_recognition as sr



def record():
    print("say now")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        a = r.recognize_google(audio)
        print(a)
        return a
        #print("system predicts:"+r.recognize_google(audio))
    except Exception:
        print("Something went wrong !!")
k=record()
print(type(k))
print(k)
