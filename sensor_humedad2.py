# Programa que genera las medidas de humedad del suelo del sensor 
import RPi.GPIO as GPIO
import time
import datetime 
import sensorh2 as sh
import signal                   
import sys
import threading
# Importaciones para Flask y Plotly
#from flask import Flask, render_template
#import pandas as pd
#import plotly.express as px
#import plotly.io as pio
#import json
#graphJSON = json.dumps(fig, cls=pio.PlotlyJSONEncoder)
#import serial

#ser = serial.Serial('/dev/ttyACM0',9600)
#ser.flushInput()

GPIO.setmode(GPIO.BCM)

channel = 17
should_blink = False
valvula_pin = 18

GPIO.setup(channel, GPIO.IN)
#GPIO.setup(valvula_pin, GPIO.OUT)
def medirHumedad():
	#lineBytes = ser.readline()
	#valor = lineBytes.decode('utf-8').strip()
	valor= GPIO.input(17)
	#def controlarValvula(valor)
	if valor== 0:
		hum,temp=sh.medirHum("humedo")
		guardarInfoSensor(hum,temp, "1")
		sh.MedidaApagado()
	else:
		hum,temp=sh.medirHum("seco")
		guardarInfoSensor(hum,temp, "0") 
		sh.Medidallenando()

def crearArchivoCSV():
	filename = "RegistroHumedadDigital.csv"
	csv = open(filename, 'w')
	csv.write("Timestamp,Humedadsuelo,Humedadambiente,Temperatura\n")
	csv.close
	
def guardarInfoSensor(hum,temp,valor):
	filename = "RegistroHumedadDigital.csv"
	humidity= (valor)
	fecha = str(datetime.datetime.now())
	humm = (hum)
	tempp = (temp)
	#dato = fecha  + "," + humidity + "," + humm + "," + tempp + "\n"
	dato = ('{},{},{},{}\n'.format(fecha,humidity,humm,tempp))
	csv = open(filename, 'a')
	csv.write(dato)
	csv.close
	

#def controlarValvula(valor):
#    if valor == 1:
#	    valvula_pin.value(1)
#	else:
#		valvula_pin(0)
		
	
def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)
def valvula_released_callback(channel):
    global should_blink
    should_blink = not should_blink
    sh.Correo()

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
    GPIO.add_event_detect(channel, GPIO.RISING, callback=valvula_released_callback, bouncetime=100)
    
    signal.signal(signal.SIGINT, signal_handler)
#    signal.pause()    

print("Sensando Humedad")
crearArchivoCSV()

#app = Flask(__name__)

#def create_plot():
 #   df = pd.read_csv('RegistroHumedadDigital.csv')  # Asegúrate de que el formato del CSV sea correcto
  #  fig= px.line(df, x='Timestamp', y=['Humedadsuelo', 'Humedadambiente', 'Temperatura'], title='Datos del Sensor de Humedad')
   # graphJSON = json.dumps(fig, cls=pio.PlotlyJSONEncoder)
    #return graphJSON

#@app.route('/')
#def index():
#    bar = create_plot()
 #   return render_template('index.html', plot=bar)

#def run_flask():
 #   app.run(host='0.0.0.0', debug=True, use_reloader=False)

# Resto del código...

#if __name__ == '__main__':
 #   flask_thread = threading.Thread(target=run_flask)
  #  flask_thread.start()
#app = Flask(__name__)

try:
    while True:
	    medirHumedad()
	    time.sleep(2)			    	    

except KeyboardInterrupt:
    print('\nFin del registro')
    GPIO.cleanup()

