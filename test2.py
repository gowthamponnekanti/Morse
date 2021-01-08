import RPi.GPIO as GPIO
import time
touch = 2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(touch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
import os
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----'}

import speech_recognition as sr
def record():
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
        return "failed"


def convert_to_morse(message):
    message=message.upper()
    dummy = ''
    for letter in message:
        if letter != ' ':  
            dummy += MORSE_CODE_DICT[letter] + ' '
        else:
            dummy += '  '
    return dummy



def morse_to_text(message):
    message += ' '

    decipher = ''
    citext = ''
    i=0
    for letter in message:
 
         
        if (letter != ' '):

            i = 0

            citext += letter
 
       
        else:
             
            i += 1
 
             
            if i == 2 :
 
                 
                decipher += ' '
            else:
 
                s=str(MORSE_CODE_DICT.values()).find(citext)
                decipher += str(MORSE_CODE_DICT.keys())[str(MORSE_CODE_DICT
                .values()).find(citext)]
                citext = ''

    return decipher



touchstatus = False

"""def read_touchsensor():
    global touchstatus
    touchstatus = GPIO.input(touch)
    print(touchstatus)
    if touchstatus:
        t1=time.time()
        print(t1)
        while(True):
            if not GPIO.input(touch):
                
                t2=time.time()
                print(t2)
                break
        t_diff=t2-t1
        print('touched')
        #time.sleep(0.15)
        return t_diff,True
    else:
        print('no')
        #time.sleep(0.15)
        return 0,False"""
    
def morse_to_vibration(result):
    n=0
    while n<len(result):
        if result[n]=='.':
            GPIO.output(18,GPIO.HIGH)
            print('.')
            time.sleep(0.25)
            GPIO.output(18,GPIO.LOW)
            time.sleep(0.25)
        elif result[n]=='-':
            GPIO.output(18,GPIO.HIGH)
            print('-')
            time.sleep(0.5)
            GPIO.output(18,GPIO.LOW)
            time.sleep(0.25)
        elif result[n]==' ':
            print('space')
            time.sleep(0.75)
        n=n+1  


"""k = 0
# Hard-coded driver function to run the program
def main():
    global k
    while 1:
        message = input('enter')
        result = convert(message.upper())
        print (result)
        #robot(message)
        #b=input('morse')
        #result = mtoa(b)
        #print (result)
        n=0
        while n<len(result):
            if result[n]=='.':
                GPIO.output(18,GPIO.HIGH)
                print('.')
                time.sleep(0.25)
                GPIO.output(18,GPIO.LOW)
                time.sleep(0.25)
                n=n+1
            elif result[n]=='-':
                GPIO.output(18,GPIO.HIGH)
                print('-')
                time.sleep(0.5)
                GPIO.output(18,GPIO.LOW)
                time.sleep(0.25)
                n=n+1
            elif result[n]==' ':
                print('space')
                time.sleep(0.75)
                n=n+1
        while True:
            if(touchstatus):
                k +=1
            if k<=2:
                GPIO.output(18,GPIO.HIGH)
                print('.')
                time.sleep(0.25)
                GPIO.output(18,GPIO.LOW)
            elif k>2:
                GPIO.output(18,GPIO.HIGH)
                print('-')
                time.sleep(0.5)
                GPIO.output(18,GPIO.LOW)"""

def generator(t_diff):
    if(t_diff<0.25 and t_diff>0):
        generated_morse_code=generated_morse_code+"."
    elif(t_diff>0.25 and t_diff<1):
        generated_morse_code=generated_morse_code+"-"
    elif(t_diff>1 and t_diff<2):
        generated_morse_code=generated_morse_code+" "
    return generated_morse_code


def main():
    t1 = 0
    t2 = 0
    k=0
    while True:
        while True:
            touchstatus = GPIO.input(touch)
            #print(touchstatus)
            if touchstatus:
                k += 1
                if k<2:
                    t1=time.time()
                    #print(t1)
                t2 = time.time()
            #else:
                #pass
                #t2=time.time()
                #print(t2)
                        
            t_diff1=t2-t1
            #print('touched')
            if(t_diff1<2):
                """print("Start")
    k=record()
        if "failed" not in k:
            q=convert_to_morse(k)
            print(q)
            morse_to_vibration(q)"""
            elif(t_diff1>2):
                print(t_diff1)
                break
        
        global touchstatus,generator_morse_code
        print('hello')
        generator_morse_code = ""
        while True:
            touchstatus = GPIO.input(touch)
            print(touchstatus)
            if touchstatus:
                y += 1
                t1=time.time()
                print(t1)
            else:
                t2=time.time()
                print(t2)
                        
            t_diff=t2-t1
            #print('touched')
            if(t_diff<2):
                gernerator_morse_code = generator(t_diff)
            elif(t_diff>2):
                break

                
                    
                
                
            
    
        
# Executes the main function
if __name__ == '__main__':
    main() 

 
