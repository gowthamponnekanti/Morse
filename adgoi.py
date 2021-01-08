import pyttsx3,time
engine = pyttsx3.init()

print(engine.getProperty('rate'))
engine.setProperty('rate',125)
engine.setProperty('volume',1)
k='hello i am nice'
engine.say(k)
engine.runAndWait()
