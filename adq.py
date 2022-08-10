# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 12:37:24 2014

@author: mariano
adq."""
import serial

import numpy as np
import time

baudios=19200
ser=serial.Serial(port='COM1', baudrate=baudios, timeout=0)

def cambiar_baudrate(new_baudios=19200):
    ser.write(('RS232:Baud ' + str(new_baudios) + '\n').encode())
    time.sleep(0.2)
    ser.baudrate=new_baudios 
    
def apagar_todo():
    """Apaga todos los canales visibles en el osciloscopio
    
    """
    ser.write(('SELECT:CH1 0; CH2 0; MATH 0; REFA 0; REFB 0\n').encode())    

def prender_ch(Chn=1):
    print('hola')
    """Activa el canal seleccionado. Toma números Int o Float.
    
    """
    #ser.write('SELECT:CH1 0; CH2 0; MATH 0; REFA 0; REFB 0\n')    
    ser.write(('SELECT:CH' + str(Chn) + ' ON' + '\n').encode())
    
def setear_ch(Chn=1, Volts=1, TriggSource=1, TriggLevel=1,
                   TimeBase='MAIn', Delay=50e-6, Time=5e-6):
    #ser.write('SELECT:CH' + str(Chn) + ' ON' + '\n')
    ser.write(('SELECT:CH' + str(Chn) + ' ON' + '\n').encode())
    ser.write(('CH' + str(Chn) + ':SCAle ' + str(Volts) + '\n').encode())
    ser.write(('TRIGger:MAIn:EDGE:SOUrce ' + 'CH' + str(TriggSource) + '\n').encode())
    ser.write(('TRIGger:MAIn:LEVel ' + str(TriggLevel) + '\n').encode())
    if TimeBase == 'MAIn':
        ser.write(('HORizontal:MODe ' + TimeBase + '\n').encode())        
        ser.write(('HORizontal:SCAle ' + str(Time/10) + '\n').encode())
    elif TimeBase == 'DELAYed':
        ser.write(('HORizontal:MODe ' + TimeBase + '\n').encode())        
        ser.write(('HORizontal:DELay:TIMe ' + str(Delay) + '\n').encode())        
        ser.write(('HORizontal:DELay:SCAle ' + str(Time/10) + '\n').encode())        
    else:
        print('Error: Pusiste cualquiera en el campo TimeBase.')

def adquirir_crudo():
    
    #start=time.time()
    junk='a'    
    while junk != b'':
        junk=ser.read(10)
    ser.write(b'CURVe?\n')
    dato_str=b''
    while len(dato_str) < 2507:
        dato_str=dato_str+ser.read(100)
    while junk != b'':
        junk=ser.read(10)
    return  dato_str[6:-1]
    
def adquirir_uno(Volts=1):
    aux_str=adquirir_crudo()        
    aux=np.frombuffer(aux_str, np.int8)
    return np.multiply(np.double(aux), np.double(Volts)*5/np.double(127))
    
def adquirir_serie(series=1, Volts=1):
    start=time.time()
    datos=np.zeros((series, 2500), np.int8)
    for i in range(0, series):
        aux_str=adquirir_crudo()        
        aux=np.frombuffer(aux_str, np.int8)
        datos[i]=aux
        print(i)
    print(time.time()-start)
    return np.multiply(np.double(datos), np.double(Volts)*5/np.double(127))
        
        #datos[i]=aux[0:2500]
   # paso=float(5)*float(Volts)/float(127)
    #datos=datos*float(paso)
    #return datos

def cerrar_y_matar(ser=ser):
    ser.close()
    
def inicializar():
    global ser
    ser=serial.Serial(port='COM1', baudrate=baudios, timeout=0)


