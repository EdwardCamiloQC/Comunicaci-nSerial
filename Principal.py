import serial
import tkinter
import threading
import time
import bitstring

from serial.serialutil import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

intervalo = 0.1
multiplicador = 1
ajuste = 10
EJE_X = 0.0
EJE_Y = 300.0
runHilo = True
flagPintado = False
datoFloat = EJE_Y
xInicial = EJE_X
yInicial = EJE_Y
xFinal = EJE_X + ajuste
yFinal = EJE_Y

def funcionAbrirSerial():
    if(puertoUART.is_open):
        try:
            puertoUART.flush()
            puertoUART.close()
            strUART.set("Cerrado")
            srtEstadoUART.set("Abrir")
        except:
            strUART.set("Error")
    else:
        try:
            puertoUART.open()
            puertoUART.flush()
            strUART.set("Abierto")
            srtEstadoUART.set("Cerrar")
        except:
            strUART.set("Error")

def funcionAumentar():
    global multiplicador
    multiplicador = multiplicador + 1
    strMult.set(multiplicador)

def funcionDisminuir():
    global multiplicador
    if(multiplicador > 1):
        multiplicador = multiplicador - 1
        strMult.set(multiplicador) 

def funcionRapido():
    global intervalo
    if(intervalo > 0):
        intervalo = intervalo - 0.001
        strMuestreo.set(intervalo)

def funcionLento():
    global intervalo
    intervalo = intervalo + 0.001
    strMuestreo.set(intervalo)

def funcionGraficar():
    global flagPintado
    flagPintado = not(flagPintado)
    if(flagPintado):
	    strPintar.set("Stop")
    else:
	    strPintar.set("Graficar")

def funcionTerminar():
    global runHilo
    runHilo = False
    try:
        puertoUART.close()
    except:
        print("No se pudo cerrar el puerto serial")
    try:
        Raiz.destroy()
    except:
        print("No se pudo cerrar la ventana")

'''--------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------'''
'''                             Creación Puero Serial                                          '''
'''--------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------'''

puertoUART = serial.Serial(port = 'COM9', baudrate = 9600, bytesize = EIGHTBITS, parity = PARITY_NONE, stopbits = STOPBITS_ONE)

'''--------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------'''
'''                                 Creación Interfaz                                          '''
'''--------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------'''

Raiz = tkinter.Tk()
Raiz.title("Micrófono")
Raiz.config(bg = '#006BDA')
Raiz.geometry("1200x600")
Raiz.resizable(False, False)

'''					Frame Control				'''

FrameControl = tkinter.Frame(Raiz)
FrameControl.config(bg = "gray", bd = 10, relief = "groove", width = "1190", height = "100")
FrameControl.grid(row = 0, column = 0, padx = 5, pady = 5)

LabelGrafica = tkinter.Label(FrameControl, text = "Gráfica", bg = "#006BDA", fg = "black", font = 10, width = 10, height = 1)
LabelGrafica.grid(row = 0, column = 0, padx = 5, pady = 5)

strPintar = tkinter.StringVar(FrameControl)
BotonGraficar = tkinter.Button(FrameControl, textvariable = strPintar, bg = "#00aaff", font = 10, width = 10, height = 1, command = funcionGraficar)
BotonGraficar.grid(row = 1, column = 0, padx = 5, pady = 5)

LabelUART = tkinter.Label(FrameControl, text = "Puerto", bg = "#006BDA", fg = "black", font = 10, width = 15, height = 1)
LabelUART.grid(row = 0, column = 1, padx = 5, pady = 5)

strUART = tkinter.StringVar(FrameControl)
EstadoSerial = tkinter.Label(FrameControl, textvariable = strUART, fg = "black", font = 10, width = 15, height = 1)
EstadoSerial.grid(row = 1, column = 1, padx = 5, pady = 5)

srtEstadoUART = tkinter.StringVar(FrameControl)
BotonPuerto = tkinter.Button(FrameControl, textvariable = srtEstadoUART, bg = "#00aaff", font = 10, width = 5, height = 1, command = funcionAbrirSerial)
BotonPuerto.grid(row = 1, column = 2, padx = 5, pady = 5)

LabelMultiplicador = tkinter.Label(FrameControl, text = "Multiplicador", bg = "#006BDA", fg = "black", font = 10, width = 15, height = 1)
LabelMultiplicador.grid(row = 0, column = 3, padx = 5, pady = 5)

strMult = tkinter.StringVar(FrameControl)
Multiplicador = tkinter.Label(FrameControl, textvariable = strMult, fg = "black", font = 10, width = 15, height = 1)
Multiplicador.grid(row = 1, column = 3, padx = 5, pady = 5)

BotonAumentarMult = tkinter.Button(FrameControl, text = "Aumentar Mult", bg = "#00aaff", font = 10, width = 15, height = 1, command = funcionAumentar)
BotonAumentarMult.grid(row = 0, column = 4, padx = 5, pady = 5)

BotonDisminuirMult = tkinter.Button(FrameControl, text = "Disminuir Mult", bg = "#00aaff", font = 10, width = 15, height = 1, command = funcionDisminuir)
BotonDisminuirMult.grid(row = 1, column = 4, padx = 5, pady = 5)

BotonAumIntervalo = tkinter.Button(FrameControl, text = "Aumentar Intervalo", bg = "#00aaff", font = 10, width = 25, height = 1, command = funcionRapido)
BotonAumIntervalo.grid(row = 0, column = 5, padx = 5, pady = 5)

BotonDisIntervalo = tkinter.Button(FrameControl, text = "Disminuir Intervalo", bg = "#00aaff", font = 10, width = 25, height = 1, command = funcionLento)
BotonDisIntervalo.grid(row = 1, column = 5, padx = 5, pady = 5)

strMuestreo = tkinter.StringVar(FrameControl)
Muestreo = tkinter.Label(FrameControl, textvariable = strMuestreo, fg = "black", font = 10, width = 15, height = 1)
Muestreo.grid(row = 0, column = 6, padx = 5, pady = 5)

BotonSalir = tkinter.Button(FrameControl, text = "Salir", bg = "#00aaff", font = 10, width = 5, height = 1, command = funcionTerminar)
BotonSalir.grid(row = 1, column = 6, padx = 5, pady = 5)

'''					Frame Vista				'''

FrameVista = tkinter.Frame(Raiz)
FrameVista.config(bg = "gray", bd = 10, relief = "groove", width = "1190", height = "480")
FrameVista.grid(row = 1, column = 0, padx = 5, pady = 5)

Grafica = tkinter.Canvas(FrameVista, width = 1150, height = 440)
Grafica.grid(row = 0, column = 0, padx = 10, pady = 10)
EjeHorizontal = Grafica.create_line(EJE_X, EJE_Y, 1150, EJE_Y, fill = '#000000', width = 2)
LineaDatos = Grafica.create_line(xInicial,yInicial,xFinal,yFinal, fill = '#00AAFF', width = 2)

'''--------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------'''
'''                                     Hilo Gráfica                                           '''
'''--------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------'''

def mostrarGrafica():
    global intervalo
    global xInicial
    global yInicial
    global xFinal
    global yFinal
    global datoFloat
    global LineaDatos
    while(runHilo):
        if(flagPintado):
            if(xFinal < 1150):
                LineaDatos = Grafica.create_line(xInicial,yInicial,xFinal,yFinal, fill = '#00AAFF', width = 2)
                xInicial = xFinal
                yInicial = yFinal
                xFinal = xFinal + ajuste
                if(puertoUART.is_open):
                    try:
                        datoBytes = puertoUART.read(size = 6)
                        datoBytes = datoBytes.strip()
                        datoFloat = float(datoBytes)
                    except ValueError:
                        puertoUART.flush()
                        datoFloat = 0
                    yFinal = EJE_Y - (datoFloat * multiplicador)
                else:
                    datoFloat = EJE_Y
                    yFinal = datoFloat
            else:
                xInicial = EJE_X
                xFinal = EJE_X + ajuste
                Grafica.delete("all")
        else:
            datoFloat = EJE_Y
            Grafica.delete("all")
            time.sleep(intervalo)

'''--------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------'''
'''                                        Principal                                           '''
'''--------------------------------------------------------------------------------------------'''
'''--------------------------------------------------------------------------------------------'''

if __name__=="__main__":
    strMult.set(multiplicador)
    strMuestreo.set(intervalo)
    if(puertoUART.is_open):
        strUART.set("Abierto")
        srtEstadoUART.set("Cerrar")
    else:
        strUART.set("Cerrado")
        srtEstadoUART.set("Abrir")
    if(flagPintado):
        strPintar.set("Stop")
    else:
        strPintar.set("Graficar")
    HiloGraficar = threading.Thread(group = None, target = mostrarGrafica, name = "Hilo1", args = (), kwargs = {}, daemon = None)
    HiloGraficar.start()
    Raiz.mainloop()