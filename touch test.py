import RPi.GPIO as GPIO
import time
touch = 2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(touch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
generated_morse_code=""

while(True):
    g = 0
    touchstatus = GPIO.input(touch)
    if touchstatus ==True:
        g=0
        while(True):
            time.sleep(0.1)
            touchstatus = GPIO.input(touch)
            if touchstatus ==True:
                g=g+0.1
            else:

                break
    print(g)
    if(g<0.25 and g>0):
        generated_morse_code=generated_morse_code+"."
    elif(g>0.25 and g<1):
        generated_morse_code=generated_morse_code+"-"
    elif(g>1 and g<2):
        generated_morse_code=generated_morse_code+" "
    elif(g>2):
        break
    gmc=generated_morse_code
    print(gmc)
    #morse_to_vibration(gmc)return g


