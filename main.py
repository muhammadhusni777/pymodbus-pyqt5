######  PROGRAM MEMANGGIL WINDOWS PYQT5 ##########################
######    WRITTEN BY : MUHAMMAD HUSNI   ##########################
######      FOR EDUCATIONAL PURPOSE     ##########################
##################################################################



####### memanggil library PyQt5 ##################################
#----------------------------------------------------------------#
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from PyQt5.QtQml import * 
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *  
import sys
import time
#----------------------------------------------------------------#


##################################################################
#----------------deklarasi variabel------------------------------#
analog = 110
input1_color = "#df1c39"
input2_color = "#df1c39"

button1_status = "0"
button2_status = "0"
button3_status = "0"

analog_output = "0"


##################################################################
#----------------mengaktifkan komunikasi modbus------------------#
import sys
import pymodbus
from pymodbus.pdu import ModbusRequest
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse
from pymodbus.transaction import ModbusRtuFramer
import serial
import threading

serial_data = ""

transmit_time = 0
transmit_time_prev = 0

data_send = ""
request = ""

holding_register = ""

print ("select your arduino port:")

def serial_ports():
    
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
print(str(serial_ports()))

port = input("write port : ")

client = ModbusClient(method='rtu', port=port, baudrate=9600, parity='N', timeout=4,strict=False)
connection = client.connect()


            

########## mengisi class table dengan instruksi pyqt5#############
#----------------------------------------------------------------#
class table(QObject):
    global analog
    def __init__(self, parent = None):
        super().__init__(parent)
        self.app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine(self)
        self.engine.rootContext().setContextProperty("backend", self)    
        self.engine.load(QUrl("main.qml"))
        sys.exit(self.app.exec_())
    
    
    
    #####################TOMBOL QML KE PYTHON###################
    @pyqtSlot(str)
    def button1(self, message):
        global button1_status
        print(message)
        button1_status = message
        

        
    @pyqtSlot(str)
    def button2(self, message):
        global button2_status
        print(message)
        button2_status = message
        
        
        
    @pyqtSlot(str)
    def button3(self, message):
        print(message)
        global button3_status
        print(message)
        button3_status = message
        
    #####################SLIDER QML KE PYTHON###################
    @pyqtSlot(str)
    def analog_output(self, message):
        global analog_output
        analog_output=message
    
    ######################KIRIM DATA ANALOG KE GAUGE##############
    @pyqtSlot(result=float)
    def get_analog(self):  return analog
    
    ####################KIRIM DATA WARNA STATUS BUTTON#############
    @pyqtSlot(result=str)
    def get_input1_color(self):  return input1_color
    
    @pyqtSlot(result=str)
    def get_input2_color(self):  return input2_color
    
    @pyqtSlot(result=str)
    def get_holding_register(self):  return holding_register
    
    

#----------------------------------------------------------------#
###############################MEMBACA DATA SERIAL##################
def modbus_data_process(num):
    global ser_bytes
    global decoded_bytes
    global serial_data
    global analog
    global data
    global input1_color
    global input2_color
    global request
    global holding_register
    while True:
        request = client.read_holding_registers(address=0,count=0x7,unit=0x1)
        try:
            print(request.registers)
            holding_register = str(request.registers)
            analog = request.registers[4]
            
            if (request.registers[5] == 0):
                input1_color = "#df1c39"
            else:
                input1_color = "#04f8fa"
           
            if (request.registers[6] == 0):
                input2_color = "#df1c39"
            else:
                input2_color = "#04f8fa"
            
        except AttributeError:
            pass
        # write registers
        client.write_register(0,int(button1_status),unit=1)
        client.write_register(1,int(button2_status),unit=1)
        client.write_register(2,int(button3_status),unit=1)
        client.write_register(3,int(analog_output),unit=1)
#----------------------------------------------------------------#



########## memanggil class table di mainloop######################
#----------------------------------------------------------------#    
if __name__ == "__main__":
    t1 = threading.Thread(target=modbus_data_process, args=(10,))
    t1.start()
    
    
    main = table()
    
    
#----------------------------------------------------------------#