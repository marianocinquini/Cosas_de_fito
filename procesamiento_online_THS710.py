# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 12:17:41 2017

@author: root
"""
import numpy as np
from numpy.fft import rfft
from scipy import signal
import scipy.io as io
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui
import pyqtgraph as pg
import adq
import datetime
import sys

Fs=50e6
T=1.0e-6
L=int(np.round(Fs*T))
cant_adq=int(sys.argv[1])
ldata=2500
mat_content=io.loadmat('Filtro_5M_50M')
filtro=mat_content['filtro']
filtro=filtro[0]
ref=1e-10
gain=1
volt_div=0.01
total_time=485.0/60

data_buffer=np.empty([cant_adq,ldata])

adq.setear_ch(Volts=volt_div, TriggSource=2, TimeBase='DELAYed')

indice_f1=3
indice_f2=8

win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

p1= win.addPlot(title="potencias vs tiempo")
p2= win.addPlot(title="nubes")

curve1 = p1.plot(symbolPen=None, pen=None, symbolSize=10, symbolBrush=(255, 255, 255, 15))
p1.setXRange(0,total_time, padding=0)
p1.setYRange(-10, 40, padding=0)

curve2= p2.plot(symbolPen=None, pen=None, symbolSize=10, symbolBrush=(255, 255, 255, 15))
p2.setXRange(0,1, padding=0)
p2.setYRange(-10, 40, padding=0)

t=QtCore.QTime()
t.start()
data=adq.adquirir_uno(volt_div)
data_buffer[0]=data
data=data[50:ldata]

data=data/gain
datafilt=signal.filtfilt(filtro,np.array([1]), data)
slots=rfft(data.reshape([int((ldata-50)/L), L]))
slots=np.absolute(slots)**2
concent=np.sum(slots[:,indice_f1:indice_f2],1)/slots.sum(1)

potencias=datafilt.reshape([int((ldata-50)/L), L])**2
potmed=10*np.log10(potencias.mean(1)/ref)
longpot=potmed.size
tiempo=np.ones(longpot)*float(t.elapsed())/1000/60

index=1
curve1.setData(tiempo,potmed)
curve2.setData(concent,potmed)

def update():
    global p1, index, tiempo, potmed, concent, longpot, gain, volt_div, filtro
    p1.enableAutoRange(enable=False)
    if (index < cant_adq):  
        index+=1
        data=adq.adquirir_uno(volt_div)
        data_buffer[index-1]=data
        data=data[50:ldata]
        data=data/gain
        datafilt=signal.filtfilt(filtro,np.array([1]), data)
        slots=rfft(data.reshape([int((ldata-50)/L), L]))
        slots=np.absolute(slots)**2
        potencias=datafilt.reshape([int((ldata-50)/L), L])**2
        potmed=np.append(potmed, 10*np.log10(potencias.mean(1)/ref))
        tiempo=np.append(tiempo, np.ones(longpot)*float(t.elapsed())/1000/60)
        concent=np.append(concent, np.sum(slots[:,indice_f1:indice_f2],1)/slots.sum(1))
        curve1.setData(x=tiempo,y=potmed)
        curve2.setData(x=concent,y=potmed)
    else:
        curve1.setData(x=tiempo,y=potmed)
        curve2.setData(x=concent,y=potmed)
        
        estampa1=str(datetime.datetime.now())
        estampa2=estampa1[0:10]+'_'+estampa1[11:13] + '-' + estampa1[14:16]
        estampa2=estampa2+ '_'+ str(int(volt_div*1e3)) + 'mV_' + str(int(Fs/1e6)) + 'MHz.txt'

        try:
            estampa2='datos/' + str(sys.argv[2])+ '_' + estampa2
        except:
            estampa2='datos/' + estampa2
               
        np.savetxt(estampa2, np.transpose(data_buffer))
        win.close()

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)


if __name__ == '__main__':

        import sys

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):

                QtGui.QApplication.instance().exec_()