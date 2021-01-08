import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import model_selection
from time import sleep
from sklearn import neighbors
import smbus            #import SMBus module of I2C          #import
import os
import RPi.GPIO as GPIO
import time
import firebase_admin,pyttsx3
from firebase_admin import credentials
from firebase_admin import db
touch = 2
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(touch,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19

CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
BCCEL_XOUT_H = 0x3B
BCCEL_YOUT_H = 0x3D
BCCEL_ZOUT_H = 0x3F
DCCEL_XOUT_H = 0x3B
DCCEL_YOUT_H = 0x3D
DCCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

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

def database():
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('/home/pi/Downloads/oops-49b91-firebase-adminsdk-hwhh0-9db96f5a05.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://oops-49b91.firebaseio.com/'})
    ref = db.reference('oops')
    print(ref)
    print(type(ref))
    if type(ref.get())=='firebase_admin.db.Reference':
        return 0
    d = dict(ref.get())
    text = next(iter(d))
    vibit = d[text]['studentName']
    speak(vibit)
    vibration(convert(vibit.upper()))
    ref.delete()

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate',150)
    engine.setProperty('volume',1)
    k= text
    engine.say(k)
    engine.runAndWait()
firebase_admin.db.Reference
import speech_recognition as sr
def record():
    print('Speak Now !!')
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        print(r.recognize_google(audio))
        vibrate(convert(r.recognize_google(audio)))
        #print("system predicts:"+r.recognize_google(audio))
    except Exception:
        print("Something went wrong !!")
    return str(r.recognize_google(audio))


def convert(message):
    dummy = ''
    for letter in message:
        if letter != ' ':
            letter.upper()
            dummy += MORSE_CODE_DICT[letter]+' '
        else:
            dummy += '  '
    return dummy

def robot(text):
    os.system("espeak'"+text+"'")

def morse_to_text(message):
    message += ' '

    decipher = ''
    citext = ''
    for letter in message:
 
         
        if (letter != ' '):

            i = 0

            citext += letter
 
       
        else:
             
            i += 1
 
             
            if i == 2 :
 
                 
                decipher += ' '
            else:
 
                 
                decipher += list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT
                .values()).index(citext)]
                citext = ''

    return decipher


def vibration(result):
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

def read_touchsensor():
    touchstatus = False
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
        elif(g>1 and g<3):
            generated_morse_code=generated_morse_code+" "
        elif(g>4):
            break
        gmc=generated_morse_code
        print(gmc)
    tt = morse_to_text(gmc)
    print(tt)
    speak(tt)


def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
   
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
   
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
   
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
   
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)
def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    #concatenate higher and lower value
    value = ((high << 8) | low)
    #to get signed value from mpu6050
    if(value > 32768):
        value = value - 65536
    return value

def ML():
    global bus,Device_Address
    while True:
        tf=pd.read_csv('gesturedataset.csv')
        x=tf.iloc[:, :-1].values
        y=tf.iloc[:, -1].values
        X_train,X_test,y_train,y_test=model_selection.train_test_split(x,y,test_size=0.5)
        knn=neighbors.KNeighborsClassifier(n_neighbors=1)
        knn.fit(X_train,y_train)
        i=0
        list1 =[]
        sleep(1.5)
        print('start')
        while i<=9:
            bus = smbus.SMBus(4)     # or bus = smbus.SMBus(0) for older version boards
            Device_Address = 0x68   # MPU6050 device address
            MPU_Init()
            acc_x = read_raw_data(ACCEL_XOUT_H)
            acc_y = read_raw_data(ACCEL_YOUT_H)
            acc_z = read_raw_data(ACCEL_ZOUT_H)
            #Full scale range +/- 250 degree/C as per sensitivity scale factor
            Ax = int(acc_x/10)
            Ay = int(acc_y/10)
            Az = int(acc_z/10)
            list1.extend([Ax,Ay,Az])
            i=i+1
            sleep(0.3)
        print(list1)
        l=np.array(list1).reshape(1,30)
        k=knn.predict(l)
        print(knn.predict_proba(l))
        print(k)
        return(k)

def main():
    g = 0
    while True:
        sleep(2)
        if ML() == 'WR':
            g +=1
            if g<2:
                database()
            else:
                re_me=record()
                a=convert(re_me.upper())
                vibration(a)
        elif (ML() == 'Water'):
            re_me=record()
            a=convert(re_me.upper())
            vibration(a)
        else:
            read_touchsensor()       
        
# Executes the main function
if __name__ == '__main__':
    main() 

