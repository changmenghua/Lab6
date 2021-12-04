from bluedot.btcomm import BluetoothClient
import RPi.GPIO as GPIO
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu

WHITE = 14
YELLOW = 15

def get_ac_info():
  data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
  voltage     =   data[0]                     / 10.0   # [V]
  current     = ( data[1] + (data[2] << 16) ) / 1000.0 # [A]
  power       = ( data[3] + (data[4] << 16) ) / 10.0   # [W]
  energy      =   data[5] + (data[6] << 16)            # [Wh]
  frequency   =   data[7]                     / 10.0   # [Hz]
  powerFactor =   data[8]                     / 100.0
  alarm       =   data[9]                              # 0 means no alarm
  return 'Voltage [V]: ' + str(voltage) + '\n' + 'Current [A]: ' + str(current) + '\n' + 'Power [W]: ' + str(power) + '\n' + 'Energy [Wh]: ' + str(energy) + '\n' + 'Frequency [Hz]: ' + str(frequency) + '\n' + 'Power factor: ' + str(powerFactor) + '\n' + 'Alarm: ' + str(alarm)

def receive_server_msg(msg):
  print("Received from server:")
  print(msg)
  if msg == "activate white socket":
    GPIO.output(WHITE, GPIO.HIGH)
    c.send("white socket activated")
  elif msg == "deactivate white socket":
    GPIO.output(WHITE, GPIO.LOW)
    c.send("white socket deactivated")
  elif msg == "activate yellow socket":
    GPIO.output(YELLOW, GPIO.HIGH)
    c.send("yellow socket activated")
  elif msg == "deactivate yellow socket":
    GPIO.output(YELLOW, GPIO.LOW)
    c.send("yellow socket deactivated")
  elif msg == "retrieve information":
    c.send(get_ac_info())
  else:
    c.send("the given command does not exist")

GPIO.setmode(GPIO.BCM)
GPIO.setup(WHITE, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
sensor = serial.Serial(
#  port='/dev/PZEM_sensor',
  port='/dev/ttyUSB0',
  baudrate=9600,
  bytesize=8,
  parity='N',
  stopbits=1,
  xonxoff=0)
master = modbus_rtu.RtuMaster(sensor)
master.set_timeout(2.0)
master.set_verbose(True)
c = BluetoothClient("phogbinh", receive_server_msg)
c.send("initiate connection")
while True:
  pass
