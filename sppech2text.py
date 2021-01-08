import speech_recognition as sr
import pyaudio
r = sr.Recognizer()

with sr.Microphone(device_index=3) as source:
    while(True):
        try:
            print('enter anything:')
            r.adjust_for_ambient_noise(source,duration=0.0001)
            audio = r.listen(source,2)
            print("System Predicts:"+r.recognize_google(audio))
            text = r.recognize_google(audio)
            print('you said : {}',format(text))
            if "breakfast" in text:
                print("I need food")
            elif "lunch" in text:
                print("I need xyz")
        except Exception:
            print("Something Wrong")


    
