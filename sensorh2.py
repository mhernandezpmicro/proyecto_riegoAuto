import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import smtplib
from email.mime.text import MIMEText

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

sensor = Adafruit_DHT.DHT11
pin = 23  # Cambia esto al número de pin GPIO al que está conectado tu sensor

Led_1 = 10
Led_2 = 9
correo_origen = 'microprocesadores2444@gmail.com'#cambiar correo
contraseña = 'fqvd uaef uuuo qecc'#colocar la contrasea de aplicación que genera gmail
correo_destino = 'm.hperez30@gmail.com'

GPIO.setup (Led_1, GPIO.OUT)
GPIO.setup (Led_2, GPIO.OUT)

def Medidallenando():
    GPIO.output(Led_1, GPIO.LOW)
    GPIO.output(Led_2, GPIO.HIGH)
      
def MedidaApagado():
    GPIO.output(Led_1, GPIO.HIGH)
    GPIO.output(Led_2, GPIO.LOW)
    
def medirHum(dato2):
    # Intenta leer los datos del sensor
    humedad, temperatura = Adafruit_DHT.read_retry(sensor, pin)

    # Verifica si la lectura fue exitosa
    if humedad is not None and temperatura is not None:
        print(f'Temperatura = {temperatura:.2f}°C, Humedad amb= {humedad:.2f}%, Humedad suel= {dato2}')
        return humedad,temperatura
    else:
        print('Error al leer el sensor. Intentando de nuevo en 3 segundos.')

    # Espera 2 segundos antes de la próxima lectura
    #time.sleep(3)

def Correo():
    msg = MIMEText("El estado de la valvula ha cambiado")
    msg['Subject'] = 'Monitoreo de la Valvula'
    msg['From'] = correo_origen
    msg["To"] = correo_destino

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(correo_origen,contraseña)
    server.sendmail(correo_origen,correo_destino,msg.as_string())
    server.quit()
