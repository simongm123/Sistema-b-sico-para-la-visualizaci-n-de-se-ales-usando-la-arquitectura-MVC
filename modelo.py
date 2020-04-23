# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 10:56:37 2020

@author: ESTEBAN MAURICIO
"""
import numpy as np
import scipy.io as sio;
import matplotlib.pyplot as plt;


from scipy.fftpack import fft;


class Biosenal(object):
    #constructor
    def __init__(self):
        self.__data=np.asarray([])#creo variables en las cuales recibire datos posteriormente desde vista grafica
        self.__canales=0
        self.__puntos=0
        
    def asignarDatos(self,data):#asigno los datos recibidos a las variables del objeto biosenal
        self.__data=data
        self.__canales=data.shape[0]
        self.__puntos=data.shape[1]
    
    #necesitamos hacer operacioes basicas sobre las senal, ampliarla, disminuirla, trasladarla temporalmente etc
    def devolver_segmento(self,x_min,x_max):
        #prevengo errores logicos
        if x_min >= x_max:
            return None
        #cojo los valores que necesito en la biosenal
        return self.__data[:,x_min:x_max]
    
    def devolver_canal(self,canal, x_min, x_max):
        #prevengo errores logicos
        if (x_min >= x_max) and (canal > self.__canales):
            return None
        #cojo los valores que necesito en la biosenal
        return self.__data[canal,x_min:x_max]
    
    
        
    def devolver_canal_filtradowelch(self,senal1,fs,ventana,solapar):
        import scipy.signal as signal;
        
        senal1= np.squeeze(senal1[0,:]);
        senal1 = senal1 - np.mean(senal1)#le quito el valor dc a la señal mediante el valor promedio
        f, Pxx = signal.welch(senal1,fs,'hamming',ventana,solapar, scaling='density');#aplico el comando signal.welch con los datos recibidos
        return f,Pxx; 
    
    def devolver_canal_filtradomulti(self,senal1,fs,fpassmenor,fpassmayor,factor,ventana,P):
        from chronux.mtspectrumc import mtspectrumc
        senal1= np.squeeze(senal1[0,:]);#tomo solamente los datos que voy a trabajar de mi señal
        senal1=senal1-np.mean(senal1);#le quito el valor dc a la señal mediante el valor promedio
        params = dict(fs = fs, fpass = [fpassmenor,fpassmayor], tapers = [factor,ventana,P], trialave = 1)
        data = np.reshape(senal1,(fs,10*5),order='F')
        Pxx, f = mtspectrumc(data, params)
        return f,Pxx;
 
    def calcularWavelet(self, senal,fs):
        
        senal= np.squeeze(senal[0,:]);
        senal = senal - np.mean(senal)
        N=senal.shape[0]
        
        import pywt #1.1.1

        
        sampling_period =  1/fs
        Frequency_Band = [4, 30] # Banda de frecuencia a analizar

        # Métodos de obtener las escalas para el Complex Morlet Wavelet  
        # Método 1:
        # Determinar las frecuencias respectivas para una escalas definidas
        scales = np.arange(1, 250)
        frequencies = pywt.scale2frequency('cmor', scales)/sampling_period
        # Extraer las escalas correspondientes a la banda de frecuencia a analizar
        scales = scales[(frequencies >= Frequency_Band[0]) & (frequencies <= Frequency_Band[1])] 
        
        N = senal.shape[0]
        
        
        # Obtener el tiempo correspondiente a una epoca de la señal (en segundos)
        time_epoch = sampling_period*N

        # Analizar una epoca de un montaje (con las escalas del método 1)
        # Obtener el vector de tiempo adecuado para una epoca de un montaje de la señal
        time = np.arange(0, time_epoch, sampling_period)
        # Para la primera epoca del segundo montaje calcular la transformada continua de Wavelet, usando Complex Morlet Wavelet

        [coef, freqs] = pywt.cwt(senal, scales, 'cmor', sampling_period)
        # Calcular la potencia 
        power = (np.abs(coef)) ** 2
        
        return time, freqs, power    