import time ,  datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import model_selection
from sklearn import neighbors
import smbus            #import SMBus module of I2C
from time import sleep          #import
import os,time
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
while True:
    tf=pd.read_csv('morsecsv.csv')
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
    m=knn.predict_proba(l)
    print(m)
    print(k)
        
