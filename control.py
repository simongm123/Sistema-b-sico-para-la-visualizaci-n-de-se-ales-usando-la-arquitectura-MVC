# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 19:12:01 2020

@author: ESTEBAN MAURICIO
"""

#el controlador enlaza todas las clases: MODELO y VISTA, CONTROLADOR
#necesito importar mi modelo y mi vista
from modelo import Biosenal
from vista_Grafica import VentanaGrafica
import sys
from PyQt5.QtWidgets import QApplication;

class Controlador(object):
    def __init__(self,vista,modelo):        
        
        self.__mi_vista=vista
        self.__mi_modelo=modelo
        
    def asignarDatos(self,datos):#conecto los datos enviados por Vista_grafica al receptor modelo
        self.__mi_modelo.asignarDatos(datos)

        
    def devolver_segmento(self, xmin, xmax):#conecto la funcion devolver segmento de modelo
         return self.__mi_modelo.devolver_segmento(xmin,xmax)
     
    def devolver_canal(self,c,xmin,xmax):#conecto la funcion devolver canal de modelo
        return self.__mi_modelo.devolver_canal(c, xmin, xmax)
     
        
    def devolver_canal_filtradowelch(self,c,fs,ventana,solapar):# conecto la vista con el modelo; con la funcion filtrado welch de modelo
        return self.__mi_modelo.devolver_canal_filtradowelch(c,fs,ventana,solapar)
    
    def devolver_canal_filtradomulti(self,c,fs,fpassmenor,fpassmayor,factor,ventana,P):# conecto la vista con el modelo; con la funcion filtrado multitaper en mi modelo
        return self.__mi_modelo.devolver_canal_filtradomulti(c,fs,fpassmenor,fpassmayor,factor,ventana,P)
    
    def calcularWavelet(self, senal,fs):# conecto la vista con el modelo; con la funcion transformada de wavelet que esta en mi modelo
        return self.__mi_modelo.calcularWavelet(senal,fs) 
    
#Donde esperamos que empiece la ejecucion
if __name__ == '__main__':
    #siempre uno y solo un QApplication
    app = QApplication(sys.argv);
    #Cuando creo la variable del tipo VentanaLogin creo el objeto que se
    #ejecutara
    mi_vista = VentanaGrafica();
    
    mi_modelo = Biosenal()
    
    #enlaza la vista y el modelo
    mi_controlador = Controlador(mi_vista, mi_modelo);
    
    #asignarle el controlador a la vista
    mi_vista.asignarControlador(mi_controlador)
    
    #siempre hay que darles a las ventanas el show para que se muestren
    mi_vista.show();
    #le decimos al QApplication que se ejecute
    sys.exit(app.exec_());

    
class Coordinador(object):
    def __init__(self,vista,biosenal):
        self.__mi_vista=vista
        self.__mi_biosenal=biosenal
    def recibirDatosSenal(self,data):
        self.__mi_biosenal.asignarDatos(data)
    def devolverDatosSenal(self,x_min,x_max):
        return self.__mi_biosenal.devolver_segmento(x_min,x_max)
    def escalarSenal(self,x_min,x_max,escala):
        return self.__mi_biosenal.escalar_senal(x_min,x_max,escala)
