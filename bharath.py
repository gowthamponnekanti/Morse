import RPi.GPIO as GPIO
import time
import os
import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import model_selection
from sklearn import neighbors
import smbus            
from time import sleep          

touch = 2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(touch,GPIO.IN,pull_up_down=GPIO.PUD_UP)

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


def record():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        a = r.recognize_google(audio)
        print(a)
        return 
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

def read_touchsensor():
    time.sleep(0.5)
    global touchstatus
    p = 0
    touchstatus = GPIO.input(touch)
    if touchstatus:
        p+=1
        if p<2:
            t1=time.time()
        t2=time.time()
        td = t2-t1
    print(td)
    return td
    
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
def main():
    global t_diff
    t_diff = 0
    while True:
        touchstatus = GPIO.input(touch)
        time.sleep(0.2)
        print(touchstatus)
        if touchstatus ==True:
            k=1
        else:
            k=0
        while k==1:
            generated_morse_code=""
            while(True):
                t_diff=read_touchsensor()
                if(t_diff<0.25 and t_diff>0):
                    generated_morse_code=generated_morse_code+"."
                elif(t_diff>0.25 and t_diff<1):
                    generated_morse_code=generated_morse_code+"-"
                elif(t_diff>1 and t_diff<2):
                    generated_morse_code=generated_morse_code+" "
                elif(t_diff>2):
                    break
            gmc=generated_morse_code
            print(gmc)
            morse_to_vibration(gmc)
            k=0
    
        """print("Start")
        k=record()
        if "failed" not in k:
            q=convert_to_morse(k)
            print(q)
            morse_to_vibration(q)
        generated_morse_code=""
        time.sleep(0.05)
        t_diff,b=read_touchsensor()
        print(t_diff)
        if(b):
            while(True):
                if(t_diff<0.25 and t_diff>0):
                    generated_morse_code=generated_morse_code+"."
                elif(t_diff>0.25 and t_diff<1):
                    generated_morse_code=generated_morse_code+"-"
                elif(t_diff>1 and t_diff<2):
                    generated_morse_code=generated_morse_code+" "
                elif(t_diff>2):
                    break
        generated_text=morse_to_text(generated_morse_code)
        print(generated_text)"""
                
                    
                
                
            
    
        
# Executes the main function
if __name__ == '__main__':
    main() 

 
