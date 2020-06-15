#pylint:skip-file

# IMPORTS
    # IMPORTS APP.PY
from repositories.projectDataRepository import projectDataRepository
from subprocess import check_output
from flask import Flask
from flask import jsonify
from flask import request
from flask_socketio import SocketIO
from flask_cors import CORS
import datetime
import Adafruit_DHT
from RPi import GPIO
import time
import threading


sensor = Adafruit_DHT.DHT11
DHT11_pin = 5

db = [16,12,25,24,23,26,19,13]
db.reverse()
RS = 21
E = 20
knop_lcd = 18
status = 0
teller = 0

magnet = 6
knop_magneet = 4
counter_magneet = 0

knop_stopw = 27
counter = 0
begin = 0
einde = 0

# BASIS INSTELLINGEN
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Wat is dit toch geheim zeg'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

endpoint = "/api/v1"


# API ENDPOINTS
@app.route(endpoint + '/x', methods=['GET'])
def read_waarden():
    if request.method == 'GET':
        return jsonify(projectDataRepository.read_alle_waarden_met_1())

@app.route(endpoint + '/oefentijd', methods=['GET'])
def read_oefentijd():
    if request.method == 'GET':
        return jsonify(projectDataRepository.read_alle_waarden_met_3())

@app.route(endpoint + '/luchtvochtigheid', methods=['GET'])
def read_luchtvochtigheid():
    if request.method == 'GET':
        return jsonify(projectDataRepository.read_alle_waarden_met_2())

@app.route(endpoint + '/waarden/<id>', methods=['GET'])
def read_alle_waarden(id):
    if request.method == 'GET':
        return jsonify(projectDataRepository.read_alle_waarden(id))


    # SENSOR DATA IN DB
def sensor_data_temp():
    while True:
        humidity, temperature = Adafruit_DHT.read(sensor, DHT11_pin)
        projectDataRepository.insert_data_temp('temp', 2, temperature)
        print("gelukt temp")
        time.sleep(60) # om de minuut een nieuwe meting in database
        

def sensor_data_lucht():
    while True:
        humidity, temperature = Adafruit_DHT.read(sensor, DHT11_pin)
        projectDataRepository.insert_data_lucht('lucht', 1, humidity)
        print("gelukt lucht")
        time.sleep(60) # om de minuut een nieuwe meting in database

        

# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('new client connect')
    socketio.emit('connected', 1)

@socketio.on('F2B_koffer_open')
def koffer_magneet():
    print("De koffer gaat open")
    lees_knop(4)
    socket.send('B2F_verandering_koffer')
    

def lees_knop(pin):
    print("button pressed")
    if GPIO.input(magnet) == 1:
        GPIO.output(magnet, GPIO.LOW)
        # res = projectDataRepository.update_status_koffer("oef", "0")
    else:
        GPIO.output(magnet, GPIO.HIGH)
        # res = projectDataRepository.update_status_koffer("oef", "1")
    data = projectDataRepository.read_status_koffer("oef")
    socket.send('B2F_verandering_koffer')
        

########## LCD CODE (ip) ############ 
# code hardware
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RS, GPIO.OUT)
    GPIO.setup(E, GPIO.OUT)
    # GPIO.setup(knop_lcd, GPIO.IN)
    GPIO.setup(knop_lcd, GPIO.IN, GPIO.PUD_UP)
    for i in db:
        GPIO.setup(i, GPIO.OUT)
    GPIO.setup(knop_stopw, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(magnet, GPIO.OUT)
    GPIO.setup(knop_magneet, GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(knop_stopw,GPIO.FALLING,callback_stopwatch,bouncetime=200)
    GPIO.add_event_detect(knop_magneet, GPIO.FALLING, callback_magneet,bouncetime=200)
    GPIO.add_event_detect(knop_lcd,GPIO.FALLING,callback_knop_lcd,bouncetime=200)


# ip adres opvragen
ip = check_output(['hostname', '--all-ip-addresses']).split()
print(ip[0].decode())


def callback_stopwatch(pin):
    global counter
    global begin
    global einde
    time.sleep(0.025)
    if GPIO.event_detected(knop_stopw):
        if counter == 0:
            print("beginnen")
            begin = time.time()
            counter = 1 
        else:
            print("stoppen")
            einde = time.time()
            res = einde - begin
            res = time.strftime('%H:%M:%S', time.gmtime(res))
            print(res)
            counter = 0 
            projectDataRepository.insert_data_oef('oef', 3, 0, res)
            

def resultaat_stopw():
    callback_stopwatch(res)

def callback_magneet(pin):
    GPIO.output(magnet, GPIO.HIGH)
    status_knop = GPIO.input(knop_magneet)
    if status_knop:
        GPIO.output(magnet, GPIO.HIGH)
        print("Koffer dicht")
    else:
        GPIO.output(magnet, GPIO.LOW)
        print("Koffer open")
        time.sleep(10)
        GPIO.output(magnet, GPIO.HIGH)


            
def lucht_temp():
    humidity, temperature = Adafruit_DHT.read(sensor, DHT11_pin)
    if humidity is not None and temperature is not None:
        print('Temperature={0}*C  Humidity={1}%'.format(temperature, humidity))
    time.sleep(3)

def set_data_bits(byte):
    mask = 0x80
    for i in range(0,8):
        GPIO.output(db[i], byte & (mask >> i))

def send_instructions(value):
    GPIO.output(RS, GPIO.LOW)
    GPIO.output(E, GPIO.HIGH)
    set_data_bits(value)
    GPIO.output(E, GPIO.LOW)
    time.sleep(0.05)

def send_character(value):
    GPIO.output(RS, GPIO.HIGH)
    GPIO.output(E, GPIO.HIGH)
    set_data_bits(value)
    GPIO.output(E,GPIO.LOW)
    time.sleep(0.2)

def init_lcd():
    send_instructions(0b00111000)
    send_instructions(0b00001111)  # cursor blinking
    send_instructions(0b00000001)

def write_message(message):
    for char in message:
        send_character(ord(char))

def callback_knop_lcd(pin):
    if GPIO.event_detected(knop_lcd):
        global teller
        global status
        status = status + 1
        teller = teller + 1
        print("Er is al {} aantal keer op de knop gedrukt".format(teller))
        if status > 4:
            status = 0
        if status == 1:
            send_instructions(0b00000001)
            ip = check_output(['hostname', '--all-ip-addresses']).split()
            print(ip)
            write_message(ip[0].decode())
            time.sleep(3)
        if status == 2:
            send_instructions(0b00000001)
            print("Luchtvochtigheid")
            humidity, temperature = Adafruit_DHT.read(sensor, DHT11_pin)
            write_message("lucht: {}%".format(humidity))
            time.sleep(3)
            if humidity < 40:
                write_message("Lucht: te laag")
            elif humidity > 70:
                write_message("Lucht: te hoog")
        if status == 3:
            send_instructions(0b00000001)
            print("Temperatuur")
            humidity, temperature = Adafruit_DHT.read(sensor, DHT11_pin)
            write_message("Temp: {}*C".format(temperature))
            time.sleep(3)
            if temperature < 12:
                write_message("Temp: te laag")
            elif temperature > 30:
                write_message("Temp: te hoog")
        if status == 4:
            send_instructions(0b00000001)
            print("Oefentijd")
            write_message("Oefentijd:")
            time.sleep(3)
####################################
setup()
init_lcd()

threading.Thread(target=sensor_data_lucht).start()
threading.Thread(target=sensor_data_temp).start()

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', debug=False)