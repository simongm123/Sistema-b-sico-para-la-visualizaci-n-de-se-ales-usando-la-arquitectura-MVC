# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
#librerias de pyQt
#librerias encargadas de recibir y morstrar informacion al usuario.
from PyQt5.QtWidgets import QMainWindow,QVBoxLayout, QFileDialog

from PyQt5.uic import loadUi
#from matplotlib.figure import Figure
import scipy.io as sio
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends. backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VentanaGrafica(QMainWindow):
    def __init__(self):
        #llamamos al constructor de la clase padre
        super(VentanaGrafica,self).__init__();
        #donde se carga el archivo designer
        loadUi('VisualizarSeñal.ui',self);
        #metodo auxilar configurar lo que queremos que "haga" la interfaz
        self.setup();
        #creamos una variable donde se encontrara la informacion a exportar
        self.__guardar=np.asarray([])
    
    
    def setup(self):
        layout = QVBoxLayout()
        #se aÃ±ade el organizador al campo grafico
        self.campo_grafico.setLayout(layout)
        #se crea un objeto para manejo de graficos
        self.__sc = MyGraphCanvas(self.campo_grafico, width=5, height=4, dpi=100)
        #se aÃ±ade el campo de graficos
        layout.addWidget(self.__sc)
        
        #se organizan las conecciones de los botones 
        self.Boton_carga.clicked.connect(self.opcion_cargar)
        self.Boton_generar.clicked.connect(self.opcion_generar)
        self.Boton_original.clicked.connect(self.opcion_original)
        self.Boton_welch.clicked.connect(self.opcion_welch)
        self.Boton_Multi.clicked.connect(self.opcion_multi)

#     
#        #hay botones que no deberian estar habilitados si no he cargado la senal 
        self.Boton_generar.setEnabled(False)
        self.Boton_original.setEnabled(False)
        self.Boton_welch.setEnabled(False)
        self.Boton_Multi.setEnabled(False)
        self.Boxmenor.setEnabled(False)
        self.Boxmayor.setEnabled(False)
        self.muestreo.setEnabled(False)
        self.tamano_ventana.setEnabled(False)
        self.solapamiento.setEnabled(False)
        self.rango_frec1.setEnabled(False)
        self.rango_frec2.setEnabled(False)
        self.factor_suav.setEnabled(False)
        self.tamano2_ventana.setEnabled(False)
        self.p.setEnabled(False)
#   
        
        
#    def opcion_graficar(self):#realiza la funcion de leer el canal que quiere viualizar 
#        canal= int(self.Seleccioncanal.text())
#        datos= self.__mi_controlador.devolver_canal(canal, self.__x_min, self.__x_max)#envia la informacion de canal a modelo y recibe la señal del canal que el usuario ingreso
#        print("Variable python: " + str(type(datos)));
#        print("Tipo de variable cargada: " + str(datos.dtype));
#        print("Dimensiones de los datos cargados: " + str(datos.shape));
#        print("Número de dimensiones: " + str(datos.shape[0]));
#        print("Tamaño: " + str(datos.size));
#        print("Tamaño de memoria (bytes): " + str(datos.nbytes));
#        self.graficar_senal(datos) #envio la señal con unico canal a graficar mediante la funcion graficar senal
        
    def opcion_cargar(self):#funcion encargada de cargar los datos que ingresara el usuario
        #se abre el cuadro de dialogo para cargar
        #* son archivos .mat
        x=str(self.Clave.toPlainText());
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir senal","","Todos los archivos (*);;Archivos mat (*.mat)*")
        if archivo != "":
            print(archivo)
            #la senal carga exitosamente entonces habilito los botones
            datamat = sio.loadmat(archivo)
            data = datamat[x]#guardo en data el archivo con la informacion correspondiente a los sensores y numero de muestras y etapas 
            #volver continuos los datos
            sensores,puntos=data.shape
            senal_continua=np.reshape(data,(sensores,puntos),order="F")
#            #el coordinador recibe y guarda la senal en su propio .py, por eso no 
#            #necesito una variable que lo guarde en el .py interfaz
#            self.__coordinador.recibirDatosSenal(senal_continua)
            self.__x_min=0
            self.__x_max=(data.shape[1])
            self.__mi_dimension=(data.shape[0])#ingreso a mi variable la dimension de canales
 #           self.Seleccioncanal.setMinimum(0)
 #           self.Seleccioncanal.setMaximum((int(self.__mi_dimension))-1)#limito mi seleccionador con el numero maximo de chanels
            #habilito los botones que anteriormente tenia desactivados
            self.Boton_generar.setEnabled(True)
            self.Boton_original.setEnabled(True)
            self.Boton_welch.setEnabled(True)
            self.Boton_Multi.setEnabled(True)
            self.Boxmenor.setEnabled(True)
            self.Boxmayor.setEnabled(True)
            self.muestreo.setEnabled(True)
            self.tamano_ventana.setEnabled(True)
            self.solapamiento.setEnabled(True)
            self.rango_frec1.setEnabled(True)
            self.rango_frec2.setEnabled(True)
            self.factor_suav.setEnabled(True)
            self.tamano2_ventana.setEnabled(True)
            self.p.setEnabled(True)
            #asigno los datos al modelo
            self.__mi_controlador.asignarDatos(senal_continua)
            datos=self.__mi_controlador.devolver_segmento(self.__x_min,self.__x_max)
            
            
            self.graficar_senal(datos)#grafico todos los canales inicialmente mediante la funcion graficar senal
#            
    def graficar_senal(self,senal):
        self.graficador.clear()
        if senal.ndim==1:#grafica un solo canal
            self.graficador.setLabel('left',text='Amplitud(mV)')
            self.graficador.setLabel('bottom',text='cantidad de muestras')
            self.graficador.plot(senal,pen=('r'))
        else:
            for canal in range (senal.shape[0]):#grafica inicialmente todos los canales
                self.graficador.setLabel('left',text='Amplitud(mV)')
                self.graficador.setLabel('bottom',text='cantidad de muestras')
                self.graficador.plot(senal[canal,:])
        self.graficador.repaint();
        
       
#    
    def opcion_generar(self):# genera la transformada de wavelet continua
        fs=int(self.muestreo.toPlainText());#recibe los datos que se encuentran en la frecuecnia de muestreo
        senal=self.__mi_controlador.devolver_segmento(self.__x_min,self.__x_max)#guardo los datos de mi señal en senal
        tiempo,freq,power=self.__mi_controlador.calcularWavelet(senal,fs) #me comunico con el controlador para enviare la informacion al modelo y recibir la transformada de wavelet
        self.__sc.graficar_espectro(tiempo, freq, power) # envio los datos al graficador para que me realice el grafico tiempo-frecuencia


    def opcion_original(self):# genera el grafio de la señal orignal graficado en la frecuencia de interes
        self.__fs=int(self.muestreo.toPlainText());#recibe la frecuencia de muestreo
        fs_res = self.__fs/self.__x_max#opera la frecuencia de muestreo sobre la cantidad de datos en la señal
        
        self.__Boxmenor=int(self.Boxmenor.text())#recibe la frecuencia de interes menor
        self.__Boxmayor=int(self.Boxmayor.text())#recibe la frecuencia de interes mayor
        self.__freqs = np.arange(0.0, self.__fs, fs_res)#crea el vector de frecuencia con el que se graficara los datos
        datos=self.__mi_controlador.devolver_segmento(self.__x_min,self.__x_max)
        datos=np.squeeze(datos[0,:])
        self.graficar_senal1(datos)#grafico todos los canales inicialmente mediante la funcion graficar senal
 
    def graficar_senal1(self,senal):#encargado de graficar los datos recibidos
        self.graficador.clear()#limpio mi ventana de graficacion
        menor=int((self.__Boxmenor)*(self.__x_max)/(self.__fs))#busca el menor munero de datos para acotar los datos ingresados en graficar
        mayor=int((self.__Boxmayor)*(self.__x_max)/(self.__fs))#busca el mayor munero de datos
        self.graficador.setLabel('left',text='Amplitud(mV)')#pongo el nombre a los ejes
        self.graficador.setLabel('bottom',text='frecuencia(Hz)')#
        self.graficador.plot(self.__freqs[menor:mayor],senal[menor:mayor])#grafica la fase vs la señal acotada porla frecuencia de interes
        self.graficador.repaint();    

    def graficar_senal2(self,senal,f):# encargado de graficar los datos para el metodo de welch y el metodo multitper
        self.graficador_2.clear()
        self.graficador_2.setLabel('left',text='Amplitud(mV)')
        self.graficador_2.setLabel('bottom',text='frecuencia(Hz)')
        menor=int((int(self.Boxmenor.text()))*(int(senal.size))/(int(f.size)))
        mayor=int((int(self.Boxmayor.text()))*(int(senal.size))/(int(f.size)))
        print(menor)
        print(mayor)
        self.graficador_2.plot(f[menor:mayor],senal[menor:mayor])#grafica la fase vs la señal acotada porla frecuencia de interes
        self.graficador_2.repaint(); 
    
    
    def opcion_welch(self):#recibe los datos aplicadole el metodo welch que se encuentra en mi modelo
        ventana=int(self.tamano_ventana.toPlainText());#recibe los datos ingresados en tamanio ventana
        solapar=int(self.solapamiento.toPlainText());#recibe los datos ingresados en el campo solapamiento
        fs=int(self.muestreo.toPlainText());
        datos=self.__mi_controlador.devolver_segmento(self.__x_min,self.__x_max)
        f,pxx=self.__mi_controlador.devolver_canal_filtradowelch(datos,fs,ventana,solapar)#me comunico con mi controlador y le envio datos fs ventana y solapar y recibo la frecuencia y la densidad de potencia
        print(f.shape)
        print(pxx.shape)
        self.graficador_2.setLabel('top',text='metodo Welch')
        self.graficar_senal2(pxx,f)#enio al graficador 2 los datos de densidad de potencia y la frecuencia para que los grafique

    def opcion_multi(self):#recibe los datos aplicadole el metodo multi que se encuentra en mi modelo
        fs=int(self.muestreo.toPlainText());#recibelos datos ingresados en el campo frecuencia de muestreo
        fpassmenor=int(self.rango_frec1.toPlainText());#recibe los datos ingresado en el campo sango frec1
        fpassmayor=int(self.rango_frec2.toPlainText());#recibe los datos ingresados en el campo rango frec2
        factor=int(self.factor_suav.toPlainText());#recibe los datos ingresados en el campo factor de suavisado
        
        ventana=int(self.tamano2_ventana.toPlainText());#recibe el tamaño de la ventana
        P=int(self.p.toPlainText());#recibe el valor P
        

        datos=self.__mi_controlador.devolver_segmento(self.__x_min,self.__x_max)
        f,pxx=self.__mi_controlador.devolver_canal_filtradomulti(datos,fs,fpassmenor,fpassmayor,factor,ventana,P)#me comunico conel controlador para que realice el metodo multitaper
        print(f.shape)
        print(pxx.shape)
        self.graficador_2.setLabel('top',text='metodo Multitaper')#grafico los datos de densidad de potencia
        self.graficar_senal2(pxx,f)
    
        
    def asignarControlador(self,c):#asigno mi controlador
        self.__mi_controlador = c
        

        
class MyGraphCanvas(FigureCanvas):
    #constructor
    def __init__(self, parent= None,width=5, height=4, dpi=100):
        
        #se crea un objeto figura
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #el axes en donde va a estar mi grafico debe estar en mi figura
        self.axes = self.fig.add_subplot(111)
        
        #llamo al metodo para crear el primer grafico
#        self.compute_initial_figure()
        
        #se inicializa la clase FigureCanvas con el objeto fig
        FigureCanvas.__init__(self,self.fig)
        
    #hay que crear un metodo para graficar lo que quiera
    def graficar_espectro(self,time, freqs, power):
        #primero se necesita limpiar la grafica anterior
        self.axes.clear()
        #ingresamos los datos a graficar
        self.axes.contourf(time,
                 freqs[(freqs >= 4) & (freqs <= 40)],
                 power[(freqs >= 4) & (freqs <= 40),:],
                 20, # Especificar 20 divisiones en las escalas de color 
                 extend='both')
        #y lo graficamos
        print("datos")
        #ordenamos que dibuje
        self.axes.figure.canvas.draw()    