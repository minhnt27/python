
import threading
import time
import sys
import datetime
import mysql.connector
from mysql.connector import Error
from random import randint
import getpass
import sys
import telnetlib
import re

class myThread (threading.Thread):
   def __init__(self,threadID,name,session_id,ip_add,username,password):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.session_id = session_id
      self.ip_add = ip_add
      self.username = username
      self.password = password
   def run(self):
      print("\nStarting thread " + self.name)
      session_work(self.name,self.session_id,self.ip_add,self.username,self.password)
      print("Exiting thread " + self.name)

def session_work(threadName,session_id, ip_add, username, password):
    print("%s: %s" % (threadName, time.ctime(time.time())))
    try:
        cmds = list_command(session_id)
        #print(cmds)
        active_session = telnet(ip_add,username,password)
        i=0
        while i < len(cmds): 
            #print(cmds[i])
            if_id=cmds[i][0]
            strcmd=cmds[i][2] + "\n"
            rx_filter=cmds[i][3]
            tx_filter=cmds[i][4]
            port=cmds[i][5]
            threshold=cmds[i][6]
            #inf = "GigabitEthernet 0/0/2"
            #strcmd = "disp trans diag interface " + inf + "\n"        
            rx_filter = 'rx *power *\(dbm\)[ :]*([-.\d]+)'
            tx_filter = 'tx *power *\(dbm\)[ :]*([-.\d]+)'
            tx_power = exce_cmd_filter(active_session, strcmd.encode(),tx_filter)
            rx_power = exce_cmd_filter(active_session, strcmd.encode(),rx_filter)
            #if rx_power == 'null': rxpower = 0
            #if tx_power == 'null': txpower = 0
            power_insert(if_id, rx_power, tx_power,threshold)
            i += 1    

        active_session.write(b"quit\n")
    except Error as e:
        print(e)
    finally:
        active_session.close()
        print(str(datetime.datetime.now()) +": close session")


def exce_cmd_filter(tn, cmd, pattern):
    try:
        #time.sleep(2) 
        tn.write(cmd)
        print("\n"+str(datetime.datetime.now()) +": exc command: "+str(cmd))
        time.sleep(2)
        line=tn.read_very_eager()
        #print(line)
        #print(str(datetime.datetime.now()) +": read result")
        #pattern = 'rx *power *\(dbm\)[ :]*([-.\d]+)'

        found = re.search(pattern, line.decode('utf8','ignore'),re.I|re.M).group(1)
    except:
        found = 'NULL'
    finally:    
        print(str(datetime.datetime.now()) +": "+ found + " dbm")
        return found


def telnet(Host, user,password):
    try:
        #user=input("Enter User name: ")
        #password=getpass.getpass()
        tn = telnetlib.Telnet(Host)
        line = tn.read_until(b"Username:")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            line = tn.read_until(b"Password:")
            tn.write(password.encode('ascii')+b"\n")
        print(str(datetime.datetime.now()) +": login OK")
    except Error as e:
        print(e)
    finally:
        return tn

def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host='localhost',database='autotester',user='root', password='Tthht@123')
        #if conn.is_connected():
        #    print('Connected to MySQL database\n')
    except Error as e:
        print(e)
    finally:
        return conn


def transceiver_select():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM rx_power ORDER BY id DESC LIMIT 5")
#        array1 = cursor.fetchall()
#        print(array1[0][2])
        row = cursor.fetchone() 
        while row is not None:
            print(row)
            row = cursor.fetchone()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def list_session():
    sessions=[]
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM session")
        sessions = cursor.fetchall()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        return sessions


def list_command(session_id):
    cmds=[]
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM config where session_id=" + str(session_id))
        cmds = cursor.fetchall()
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        return cmds

def power_insert(if_id, rx, tx, threshold):
    query = "INSERT INTO rx_power(if_id,rx_power,tx_power,threshold) " \
            "VALUES(%s,%s,%s,%s)"
    args = (if_id, rx, tx, threshold)
 
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(query, args)
        if cursor.lastrowid:
            print('insert db, id:', cursor.lastrowid)
        else:
            print('\nlast insert id not found') 
        conn.commit()
    except Error as e:
        print(e) 
    finally:
        cursor.close()
        conn.close()

def routine():
    print ("Starting Main Thread\n")
    print(time.ctime())
    #threading.Timer(300, routine).start()
    sessions = list_session()
    #print(sessions)
    i=0
    thread=[]
    while i < len(sessions): 
        thread.append(i)
        #print(sessions[i])
        session_id=sessions[i][0]
        ip_add=sessions[i][1]
        username=sessions[i][2]
        password=sessions[i][3]
        
        # Create new threads
        thread[i] = myThread(i+1000, "telnet_session_"+str(i+1), session_id, ip_add, username, password)
        # Start new Threads
        thread[i].start()
        i += 1    
    time.sleep(30)
    print ("Exiting Main Thread\n")

routine()