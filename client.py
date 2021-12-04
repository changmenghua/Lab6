from bluedot.btcomm import BluetoothClient
import serial
import modbus_tk.defines as cst
from modbus_tk import modbus_rtu
import time
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.output(2, GPIO.LOW)
GPIO.output(3, GPIO.LOW)

def data_received(data):
    print(data)
    if data == "start":
        sleep(2)
        print("receive start!")

        GPIO.output(2, GPIO.HIGH)
        GPIO.output(3, GPIO.HIGH)
        time.sleep(2)
        sensor = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        bytesize=8,
        parity='N',
        stopbits=1,
        xonxoff=0
        )

        master = modbus_rtu.RtuMaster(sensor)
        master.set_timeout(2.0)
        master.set_verbose(True)
        sleep(2)
        data = master.execute(1, cst.READ_INPUT_REGISTERS, 0, 10)
        voltage = data[0] / 10.0 # [V]
        current = (data[1] + (data[2] << 16)) / 1000.0 # [A]
        power = (data[3] + (data[4] << 16)) / 10.0 # [W]
        energy = data[5] + (data[6] << 16) # [Wh]
        frequency = data[7] / 10.0 # [Hz]
        powerFactor = data[8] / 100.0
        alarm = data[9] # 0 = no alarm
        print('Voltage [V]: ', voltage)
        print('Current [A]: ', current)
        print('Power [W]: ', power) # active power (V * I * power factor)
        print('Energy [Wh]: ', energy)
        print('Frequency [Hz]: ', frequency)
        print('Power factor []: ', powerFactor)
        print('Alarm : ', alarm)
        # Changing power alarm value to 100 W
        # master.execute(1, cst.WRITE_SINGLE_REGISTER, 1,output_value=100)
        try:
            master.close()
            if sensor.is_open:
                sensor.close()
        except:
            pass

        datas = ''
        voltage = str(voltage)
        current = str(current)
        power = str(power)
        energy = str(energy)
        freq = str(frequency)
        pF = str(powerFactor)
        alarm = str(alarm)
        datas += "vol:"
        datas += voltage
        datas += "\n"
        datas += "current:"
        datas += current
        datas += "\n"
        datas += "power:"
        datas += power
        datas += "\n"
        datas += "energy:"
        datas += energy
        datas += "\n"
        datas += "freq:"
        datas += freq
        datas += "\n"
        datas += "pF:"
        datas += pF
        datas += "\n"
        datas += "Alarm:"
        datas += alarm

        c.send(datas)


c = BluetoothClient("raspberrypichihya", data_received)

while(True):
    pass