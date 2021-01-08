import RPi.GPIO as GPIO
import time
touch = 2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(touch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
touchstatus=False
while 1:
    touchstatus = GPIO.input(touch)
    time.sleep(0.1)
    if touchstatus:
        print('on')
    else:
        print('---')
