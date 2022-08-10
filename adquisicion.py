#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 29 16:35:51 2014

@author: mariano
"""
import sys
import adq
import numpy as np
import datetime
import time

f=open('conf1.txt','r')
Chn=int(f.readline())
print(f.readline(), Chn, '\n')

Volts=float(f.readline()) 
print(f.readline(), Volts, '\n')

TrgS=int(f.readline())
print(f.readline(), TrgS, '\n')

TrgV=float(f.readline())
print(f.readline(), TrgV, '\n')

TimeB=f.readline().split('\n')[0]
print(f.readline(), TimeB, '\n')

delay=float(f.readline())
print(f.readline(), delay, '\n')

horiz=float(f.readline())
print(f.readline(), horiz, '\n')

f.close()

series=int(sys.argv[1])
adq.cambiar_baudrate(19200)
adq.apagar_todo()
adq.setear_ch(Chn, Volts, TrgS, TrgV, TimeB, delay, horiz)
time.sleep(4)
dato=adq.adquirir_serie(series,Volts)

estampa1=str(datetime.datetime.now())
estampa2=estampa1[0:10]+'_'+estampa1[11:13] + '-' + estampa1[14:16]

Fs=2500.0/(10.0*horiz)

estampa3=estampa2+ '_'+ str(int(Volts*1e3)) + 'mV_' + str(int(Fs/1e6)) + 'MHz.txt'

try:
    estampa3='datos/' + str(sys.argv[2])+ '_' + estampa3
except:
    estampa3='datos/' + estampa3    
    
np.savetxt(estampa3, np.transpose(dato))

