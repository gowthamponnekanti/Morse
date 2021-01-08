from espeak import espeak
def espeak(text):
    espeak.synth(text)
text = 'this is a test'
espeak(text)
