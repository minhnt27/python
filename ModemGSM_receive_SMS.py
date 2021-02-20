import serial
import time
import re
from pprint import pprint
class TextMessage:
    def connectPhone(self):
        #update the COM port, others should not change for SR2MOD02
        self.ser = serial.Serial(port='COM4', baudrate=115200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=1, timeout=5, dsrdtr=True) 
        time.sleep(1)

    def list(self):
        self.ser.write(b'ATZ\r')
        self.ser.write(b'ATE0\r')
        time.sleep(1)
        self.ser.write(b'AT+CMGF=1\r')# put in textmode
        time.sleep(1)
        self.ser.write(b'''AT+CMGL="ALL"''' + b'\r') #fetch all sms's
        list = self.ser.readlines()
        result=[]
        for msg in list:
            print(msg.decode('utf8','ignore'))
            if "+CMGL" in msg.decode('utf8','ignore'): #+CMGL looks for all SMS messages
                result.append(re.findall("(?:^|,)(\"(?:[^\"]+|\"\")*\"|[^,]*)", msg.decode('utf8','ignore')))
                #print(msg.decode('utf8','ignore'))
        return result
                
    def read(self,idmsg):
        self.ser.write(b'ATZ\r')
        time.sleep(1)
        self.ser.write(b'AT+CMGF=1\r')# put in textmode
        time.sleep(1)
        atcmd='AT+CMGR=' + str(idmsg) + '\r'
        self.ser.write(atcmd.encode())
        read = self.ser.readlines()
        for msg in read:
            if (msg != b"\r\n") and (msg != b"OK\r\n"):
                print(msg)

    def delAll(self):
        self.ser.write(b'ATZ\r')
        time.sleep(1)
        self.ser.write(b'ATZ\r AT+CMGD=1,4\r')

    def disconnectPhone(self):
        self.ser.close()


try:
    sms = TextMessage()
    sms.connectPhone()
    
    #print all sms info
    result=sms.list()
    pprint(result)
    
    #print the last sms
    count=len(result)
    if count>0:
        lastmsg=result[count-1]
        header=lastmsg[0]
        idmsg=str(header).split(":")
        sms.read(idmsg=idmsg[1].strip())
    
    #delete all sms
    sms.delAll()
finally:
    if sms:
        sms.disconnectPhone()