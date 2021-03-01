#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to respond to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import sys
import json
import logging

from telegram.utils.request import Request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

import sqlite3
import mysql.connector
import pandas as pd


#tttm
db_file=r"D:\minhnt27\chatbot\chatbotlog.db"
log_path=r"D:\minhnt27\chatbot\\"
GroupId='-322186504'
host_ip='localhost'
TOKEN="1462992536:AAGH0_AJ09IkGpQV0L0gU3YqdfjAnVHVWTk"
AdminId='996634566'

#minhnt27
#db_file=r"C:\Users\NhatVQ\Desktop\minhnt27\chatbotlog.db"
#log_path=r"C:\Users\NhatVQ\Desktop\minhnt27\\"
#GroupId='-322186504'
#host_ip='192.168.0.199'
#TOKEN="1479164645:AAHmcT6W_c_noexGinNWfTvrMBMsGFTSTPw"

#=========================================
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

#====================================
#sqlite


#replication mysql tttm
#host_ip='localhost'
db_tttm='hht20180903'
def connect():
    """ Connect to MySQL database """
    try:
        conn = mysql.connector.connect(host=host_ip,database=db_tttm,user='tableau', password='Tthht@123')
        #if conn.is_connected():
        #    print('Connected to MySQL database\n')
    except mysql.Error as e:
        print(e)
    finally:
        return conn


#proxy sql ->mysql ibms
host_bms='192.168.0.180'
db_bms='historianbms'

def connectbms():
    """ Connect to MySQL iBMS database """
    try:
        conn = mysql.connector.connect(host=host_bms,port='6033',database=db_bms,user='backup', password='Tthht@123')
        #if conn.is_connected():
        #    print('Connected to MySQL database\n')
    except mysql.Error as e:
        print(e)
        return False
    finally:
        return conn

#========================================
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    update.message.reply_text('Hi! Tôi là chatbot của TTr.HHT, cũng có thể tôi giúp được bạn vài thứ, thử gõ /help ')
    updateuser(update.message.chat.id, update.message.chat.first_name, update.message.chat.last_name)


def login(chatid):
    try:
        conn = sqlite3.connect(db_file)
        db_df = pd.read_sql_query(f"Select id from config where chatid ='{chatid}' and (datetime(expired) >=datetime('now') or (expired IS NULL))", conn)
        if db_df.id.count()==0:
            return False
        return True
    except Exception as e:
        print(e)
    finally:
        conn.close() 


def grant_command(update: Update, context: CallbackContext) -> None:
    print("grant:")
    if (login(update.message.chat.id)):
        update.message.reply_text('Bạn đã có quyền đăng nhập')
        return
    update.message.reply_text('Bạn vừa gửi yêu cầu đăng nhập đến Admin, vui lòng đợi phản hồi')
    data = {
        "chatid": update.message.chat.id,
        #"firstname": update.message.chat.first_name,
        #"lastname": update.message.chat.last_name
        }
    data1={
        "command":"Aprove",
        "data":data
        }
    data2={
        "command":"Temp2h",
        "data":data
        }
    data3={
        "command":"Reject",
        "data":data
        }
    keyboard = [
                [
                    InlineKeyboardButton("Aprove", callback_data=json.dumps(data1)),
                    InlineKeyboardButton("Temp2h", callback_data=json.dumps(data2)),
                    InlineKeyboardButton("Reject", callback_data=json.dumps(data3)),
                ],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=AdminId
                             ,text=f"{update.message.chat.id}-{update.message.chat.first_name} {update.message.chat.last_name} gửi yêu cầu đăng nhập:"
                             ,reply_markup=reply_markup)   


def register(chatid, expired):
    """ Connect to SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        c=conn.cursor()
        #insert data       
        #Sqlite: datetime(time) >=datetime('now', '-4 Hour')
        data_sql = """Select * from config where chatid = ?"""
        datatuple = (chatid,)
        c.execute(data_sql,datatuple)
        found = c.fetchall()
        if len(found)==0:
            data_sql = """INSERT INTO config(chatid) VALUES (?)"""
            datatuple = (chatid,)  
            c.execute(data_sql,datatuple)
        if (expired == 0):
            data_sql = """UPDATE config SET expired=NULL WHERE chatid=?"""
            datatuple = (chatid,)  
            c.execute(data_sql,datatuple)        
        elif (expired > 0):
            data_sql = """UPDATE config SET expired=datetime('now', '+2 Hour') WHERE chatid=?"""
            datatuple = (chatid,)  
            c.execute(data_sql,datatuple)
        else:
            print("expired có vấn đề")
        conn.commit()
        c.close()
    except sqlite3.Error as e:
        print(e)
        #create table
        create_table_sql = """CREATE TABLE IF NOT EXISTS config
                 (id INTEGER PRIMARY KEY,
                  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  chatid varchar(20) NOT NULL,
                  nodeaudit text, firstname text, lastname text,
                  expired DATETIME NULL DEFAULT NULL)"""
        c.execute(create_table_sql)
    finally:
        conn.close()    
        

def revoke_command(update: Update, context: CallbackContext) -> None:
    """ Connect to SQLite database """
    try:
        if (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /revoke user_id")
            return
        chatid=context.args[0]
        conn = sqlite3.connect(db_file)
        c=conn.cursor()
        #delete data
        data_sql = """DELETE FROM config WHERE chatid=?"""
        datatuple = (chatid,)        
        c.execute(data_sql,datatuple) 
        #select data
        data_sql = """select * from config WHERE chatid=?"""
        datatuple = (chatid,)        
        c.execute(data_sql,datatuple)
        found = c.fetchall()
        conn.commit()
        c.close()
        if len(found)==0:
            update.message.reply_text(f"Đã xóa user. Không còn user với id={chatid}")
            return True
        else:
            update.message.reply_text("Không xóa được user, vui lòng kiểm tra")
            return False
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()


def updateuser(chatid, firstname, lastname):
    """ Connect to SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        data_sql = """Select * from config where chatid = ?"""
        datatuple = (chatid,)
        c.execute(data_sql,datatuple)
        found = c.fetchall()
        if len(found)==0:
            pass
            #insert data
            #data_sql = """INSERT INTO config(chatid,firstname,lastname) VALUES (?,?,?)"""
            #datatuple = (chatid,firstname,lastname)        
            #c.execute(data_sql,datatuple) 
        else:
            #update data
            data_sql = """UPDATE config set firstname=?,lastname=? where chatid=?"""
            datatuple = (firstname,lastname,chatid)        
            c.execute(data_sql,datatuple)
        conn.commit()
        c.close()
    except sqlite3.Error as e:
        print(e)
    finally:
        if (conn):
            conn.close()

#==========================================
def debug_log(update):
    logging.info("debug:")
    print(str(update.message.chat.id) + "-" + str(update.message.chat.first_name) + "-" + str(update.message.chat.last_name))
    print(str(update.message.text))

def debug_save(update):
    """ Connect to SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        insert_log_sql = """INSERT INTO debuglog (chatid, firstname, lastname, data) VALUES (?,?,?,?)"""
        #datatuple=(chatid, firstname, lastname, data)
        datatuple=(update.message.chat.id, update.message.chat.first_name, update.message.chat.last_name, update.message.text)
        c.execute(insert_log_sql,datatuple)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        #create table
        create_table_sql = """CREATE TABLE IF NOT EXISTS debuglog
                 (id INTEGER PRIMARY KEY,
                  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  chatid varchar(20) NOT NULL,
                  firstname text,
                  lastname text,
                  data text,
                  note text)"""
        c.execute(create_table_sql)    
    finally:
        if (conn):
            conn.close()

#====================================
def nodes_select(nodename, limitrows):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT n.id, n.name as Nodename, r.name as Phongmay FROM nodes n "
                       + "left join rooms r on n.room_id=r.id "
                       + "WHERE n.node_status_id<7 and n.name like '%" + nodename + "%' limit " + str(limitrows))
        data = cursor.fetchall()
        for row in data:
            print(row)
        #return json.dumps(data, indent = 1, ensure_ascii=False)
        return data
    except mysql.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def nodes_select2(nodename, limitrows):
    try:
        conn = connect()
        db_df = pd.read_sql_query("SELECT n.id, n.name as Nodename, r.name as Phongmay FROM nodes n "
                       + "left join rooms r on n.room_id=r.id "
                       + "WHERE n.node_status_id<7 and n.name like '%" + nodename + "%' limit " + str(limitrows)
                       , conn)
        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return data
    except Exception as e:
        print(e)
    finally:
        conn.close()

#===========================================
def who_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /who is issued."""
    debug_log(update)
    try:
        update.message.reply_text('Tôi là chatbot, tôi liên kết với pmTTTM của TTr.HHT để giúp bạn một vài thông tin cơ bản một cách nhanh chóng nhất, hãy gõ /help')
    except Exception as e:
        print(e)

#======================================
def dellog_command(update: Update, context: CallbackContext) -> None:
    debug_log(update)
    try:
        delete_log(str(update.message.chat.id))
        update.message.reply_text("Log của bạn đã được xóa")
    except Exception as e:
        print(e)

def delete_log(chatid):
    """ Connect to SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        #delete data
        delete_data_sql = """delete from assetschecklog where chatid like ? """
        datatuple = (chatid,)
        c.execute(delete_data_sql,datatuple)
        conn.commit()
        c.close()
    except sqlite3.Error as e:
        print(e)   
    finally:
        if (conn):
            conn.close()

#========================================
def getlog_command(update: Update, context: CallbackContext) -> None:
    debug_log(update)
    try:
        getcsv(update.message.chat.id)
        document = open(log_path + str(update.message.chat.id) + ".xlsx", 'rb')
        update.message.reply_document(document=document)
    except Exception as e:
        print(e)

def getcsv(chatid):
    try:
        conn = sqlite3.connect(db_file)
        db_df = pd.read_sql_query("SELECT *, datetime(time,'localtime') FROM assetschecklog where chatid like '" + str(chatid) + "'", conn)
        db_df.to_excel(log_path + str(chatid) + ".xlsx", index=False, encoding="utf-8")
    except Exception as e:
        print(e)

#==========================================
def check(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    try:
        limitrows = 5
        result = assets_check(update.message.text, limitrows)
        update.message.reply_text(f"Kiểm kê serial: {update.message.text}. Kết quả:\n"
                                  + result.replace('"','')
                                  )
        #update.message.reply_text(result.replace('"',''))
        assetschecklog(update.message.chat.id,update.message.text,result)
    except Exception as e:
        print(e)

def assets_check(serial, limitrows):
    try:
        conn = connect()
        db_df = pd.read_sql_query("SELECT a.serial as Serial, avc.code as MãVHKT, avc.name as TênVHKT, wh.name as Vịtrí, concat(cha.name,'/',cs.name) as ChassSlot "
                       + "FROM assets a "
                       + "left join asset_vhkt_codes avc on a.asset_vhkt_code_id=avc.id "
                       + "left join warehouses wh on a.warehouse_id=wh.id "
                       + "left join modules mo on a.id=mo.asset_id "
                       + "left join chassis_slots cs on cs.id=mo.chassis_slot_id "
                       + "left join chassis cha on cha.id=mo.chassis_id "
                       + "WHERE a.asset_position_id <=5 and a.serial like '" + serial + "' limit " + str(limitrows)
                      , conn)
        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return json.dumps(data, indent = 1, ensure_ascii=False)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def assetschecklog(chatid,serial,result):
    print("\n" + str(chatid) + " , " + serial + " , " + result)
    insert_log(str(chatid), serial, result) 

def insert_log(chatid, serial, result):
    """ Connect to SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        #print("Connected to SQLite")
        #insert log
        insert_log_sql = """INSERT INTO assetschecklog (chatid, serial, result) VALUES (?,?,?)"""
        datatuple = (chatid, serial, result)
        c.execute(insert_log_sql,datatuple)
        #insert audit
        
        insert_audit_sql = """UPDATE audit SET checked=? WHERE chatid like ? and serial like ?"""
        datatuple = (result, chatid, serial)
        c.execute(insert_audit_sql,datatuple)

        conn.commit()
        #print("Python Variables inserted successfully into SqliteDb_developers table")
        c.close()
    except sqlite3.Error as e:
        print(e)
        #create table
        #c.execute('PRAGMA encoding="UTF-8";')
        create_table_sql = """CREATE TABLE IF NOT EXISTS assetschecklog
                 (id INTEGER PRIMARY KEY,
                  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  chatid varchar(20) NOT NULL,
                  serial varchar(20) NOT NULL,
                  result text )"""
        c.execute(create_table_sql)    
    finally:
        if (conn):
            conn.close()

#=======================================
def where_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /where is issued."""
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    try:
        limitrows = 5
        if (len(context.args))>1:
            if context.args[1].isnumeric():
                limitrows = int(context.args[1])
        elif (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /where tên_node")
            return
        result = nodes_select2(context.args[0], limitrows)
        print(result)
        l = len(result)
        if l == 1:
            rackresult=rackloc(result[0]['id'])
            result=json.dumps(result, indent = 1, ensure_ascii=False)
            update.message.reply_text("Vị trí node: \n" + result.replace('"',''))
            print(rackresult)
            update.message.reply_text("Vị trí rack: \n" + rackresult.replace('"',''))
        elif l>1:
            result=json.dumps(result, indent = 1, ensure_ascii=False)
            update.message.reply_text("Vị trí node: " + result.replace('"','')
                                      +"\nĐể biết tọa độ chi tiết của rack bạn cần chính xác tên node"
                                      )
        else:
            update.message.reply_text("Không tìm thấy node bạn yêu cầu")
        updateuser(update.message.chat.id, update.message.chat.first_name, update.message.chat.last_name)
    except Exception as e:
        print(e)

def rackloc(node_id):
    try:
        conn = connect()
        db_df = pd.read_sql_query("SELECT con.id FROM equipment eq "
                                   + "left join chassis ch on ch.id=eq.chassis_id "
                                   + "left join containers con on con.id= ch.container_id "
                                   + "WHERE eq.node_id =" + str(node_id) 
                                   + " group by con.id"
                                   , conn)
        result=db_df.to_json(orient="records", date_format='iso')
        rack = json.loads(result)
        if len(rack)==0:
            return "Node chưa liên kết với rack thiết bị nên không có thông tin rack chi tiết"        
        data=[]
        for row in rack:
            db_df = pd.read_sql_query("SELECT con.name as TenRack, la.name as Phongmay, CONCAT(ro.name, con.xpos) as Toado "
                                       + "from containers con "
                                       + "left join `rows` ro on ro.id=con.row_id "
                                       + "left join layers la on la.id=con.layer_id "
                                       + "WHERE con.row_id=ro.id and con.id=" + str(row['id'])
                                       , conn)           
            result=db_df.to_json(orient="records", date_format='iso')
            rackloc = json.loads(result)
            data.append(rackloc[0])
        return json.dumps(data, indent = 1, ensure_ascii=False)
    except Exception as e:
        print(e)
    finally:
        conn.close()

#=============================================
def audit_command(update: Update, context: CallbackContext) -> None:
    """Audit"""
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    try:
        limitrows = 5
        if (len(context.args))>1:
            if context.args[1].isnumeric():
                limitrows = int(context.args[1])
        elif (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /audit tên_node")
            return
        
        nodeaudit = nodes_select(context.args[0], limitrows)
        print(nodeaudit[0][1])
        
        nodeaudit = nodes_select2(context.args[0], limitrows)
        print(nodeaudit[0]['Nodename'])
        l = len(nodeaudit)
        if l == 1:
            nodeauditset(update.message.chat.id,str(nodeaudit[0]['Nodename']))
            totalserial=assetsload(update.message.chat.id, str(nodeaudit[0]['Nodename']))
            update.message.reply_text("Bắt đầu kiểm kê node:" + str(nodeaudit[0]['Nodename']) 
                                      + ". Node có tổng số serial là:"+ str(totalserial[0][0]) 
                                      + ". Hoặc set lại để kiểm kê node khác. Sau khi kiểm kê, lấy log file audit bằng /auditlog")
        elif l>1:
            result=json.dumps(nodeaudit, indent = 1, ensure_ascii=False)
            update.message.reply_text("Vị trí node: \n"
                                      + result
                                      + "\nĐể audit bạn cần chính xác tên node"
                                      )
            
            #update.message.reply_text(result)
            #update.message.reply_text("Để audit bạn cần chính xác tên node")
        else:
            update.message.reply_text("Không tìm thấy node bạn yêu cầu")            
    except Exception as e:
        print(e)

def assetsload(chatid, nodename):
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT a.serial, avc.code, avc.name, wh.name "
                       + "FROM assets a "
                       + "left join asset_vhkt_codes avc on a.asset_vhkt_code_id=avc.id "
                       + "left join warehouses wh on a.warehouse_id=wh.id "
                       + "WHERE a.asset_position_id <=5 and wh.name like '" + nodename + "'")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        #import local database
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        #del old data
        del_data_sql="""DELETE FROM audit WHERE chatid like ?"""
        datatuple = (chatid,)
        c.execute(del_data_sql,datatuple)
        #insert new data
        insert_data_sql = """INSERT INTO audit(chatid,serial,vhktcode,vhktname,node) VALUES (?,?,?,?,?)"""
        #c.executemany(insert_data_sql,data)
        for row in data:
            datatuple = (chatid,row[0],row[1],row[2],row[3])        
            c.execute(insert_data_sql,datatuple)
        conn.commit()
        select_data_sql="""select count(*) FROM audit WHERE chatid like ?"""
        datatuple = (chatid,)
        c.execute(select_data_sql,datatuple)
        totalserial = c.fetchall()
        c.close()
        conn.close()
        return totalserial
    except mysql.Error as e:
        print(e) 
    finally:                       
        conn.close()

def nodeauditset(chatid,nodeaudit):
    """ Connect to SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()        
        #update data
        data_sql = """UPDATE config SET nodeaudit=? Where chatid = ?"""        
        datatuple = (nodeaudit, chatid)        
        c.execute(data_sql,datatuple)
        conn.commit()
        c.close()
    except sqlite3.Error as e:
        print(e)
    finally:
        if (conn):
            conn.close() 

#===========================================
def getaudit_command(update: Update, context: CallbackContext) -> None:
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    try:
        checkedcount=getcsvaudit(update.message.chat.id)
        document = open(log_path + str(update.message.chat.id) + "_audit.xlsx", 'rb')
        #update.message.reply_text("Bạn đã kiểm kê được: " + checkedcount + " serial. Chi tiết xem file đính kèm")
        update.message.reply_document(document=document
                                      , caption="Bạn đã kiểm kê được: " 
                                                + checkedcount 
                                                + " serial. Chi tiết xem file đính kèm")
    except Exception as e:
        print(e)

def getcsvaudit(chatid):
    try:
        conn = sqlite3.connect(db_file)
        db_df = pd.read_sql_query("SELECT *, datetime(time,'localtime') FROM audit where chatid like '" + str(chatid) + "'", conn)
        db_df.to_excel(log_path + str(chatid) + "_audit.xlsx", index=False)
        #print(db_df.count())
        #print(db_df.serial.count())
        #print(db_df.checked.count())
        return str(db_df.checked.count())+"/"+str(db_df.serial.count())
    except Exception as e:
        print(e)

#===================================
def serial_command(update: Update, context: CallbackContext) -> None:
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    """Send a message when the command /serial is issued."""
    debug_log(update)
    try:
        limitrows = 5
        if (len(context.args))>1:
            if context.args[1].isnumeric():
                limitrows = int(context.args[1])
        elif (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /serial mẫu_serial")
            return
        update.message.reply_text(f"Tìm tài sản:*{context.args[0]}*")
        result = assets_select(context.args[0], limitrows)
        update.message.reply_text(result.replace('"',''))    
    except Exception as e:
        print(e)

def assets_select(serial, limitrows):
    try:
        conn = connect()
        db_df = pd.read_sql_query("SELECT a.serial as Serial, avc.code as MãVHKT, avc.name as TênVHKT, wh.name as Vịtrí "
                       + "FROM assets a "
                       + "left join asset_vhkt_codes avc on a.asset_vhkt_code_id=avc.id "
                       + "left join warehouses wh on a.warehouse_id=wh.id "
                       + "WHERE a.asset_position_id <=5 and a.serial like '%" + serial + "%' limit " + str(limitrows)
                      , conn)
        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return json.dumps(data, indent = 1, ensure_ascii=False)
    except Exception as e:
        print(e)
    finally:
        conn.close()

#====================================
def spare_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /sparetb is issued."""
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    try:
        limitrows = 5
        if (len(context.args))>1:
            if context.args[1].isnumeric():
                limitrows = int(context.args[1])
        elif (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /sparetb mã_hàng_hóa")
            return
        update.message.reply_text("Tìm UCTT BanTB:")
        result = spare_list(context.args[0], limitrows)
        update.message.reply_text(result.replace('"','')) 
    except Exception as e:
        print(e)

def spare_list(code, limitrows):
    try:
        conn = connect()
        db_df = pd.read_sql_query("SELECT a.serial as Serial, avc.code as MãVHKT, avc.name as TênVHKT, wh.name as Vịtrí, a.note FROM assets a "
                        + "left join asset_vhkt_codes avc on a.asset_vhkt_code_id=avc.id "
                        + "left join warehouses wh on a.warehouse_id = wh.id "
                        + "WHERE a.serial is not null and a.asset_position_id<=5 " 
                        + "and wh.id in (300, 3422, 3524, 3846, 3837, 3847) "
                        + "and (avc.code like '%" + code + "%' or avc.name like '%" + code + "%') limit " + str(limitrows)
                      , conn)
        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return json.dumps(data, indent = 1, ensure_ascii=False)
    except Exception as e:
        print(e)
    finally:
        conn.close()

#========================================
def sparetd_command(update: Update, context: CallbackContext) -> None:
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    """Send a message when the command /sparetd is issued."""
    debug_log(update)
    try:
        limitrows = 5
        if (len(context.args))>1:
            if context.args[1].isnumeric():
                limitrows = int(context.args[1])
        elif (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /sparetd mã_hàng_hóa")
            return
        update.message.reply_text("Tìm UCTT BanTD:")
        result = sparetd_list(context.args[0], limitrows)
        update.message.reply_text(result.replace('"','')) 
    except Exception as e:
        print(e)

def sparetd_list(code, limitrows):
    try:
        conn = connect()
        db_df = pd.read_sql_query("SELECT a.serial as Serial, avc.code as MãVHKT, avc.name as TênVHKT, wh.name as Vịtrí FROM assets a "
                        + "left join asset_vhkt_codes avc on a.asset_vhkt_code_id=avc.id "
                        + "left join warehouses wh on a.warehouse_id = wh.id "
                        + "WHERE a.serial is not null  and a.asset_position_id<=5 "
                        + "and wh.id in (3579,3671) "
                        + "and (avc.code like '%" + code + "%' or avc.name like '%" + code + "%') limit " + str(limitrows)
                      , conn)

        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return json.dumps(data, indent = 1, ensure_ascii=False)
    except Exception as e:
        print(e)
    finally:
        conn.close()


#===========================================
def node_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /node is issued."""
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    try:
        limitrows = 5
        if (len(context.args))>1:
            if context.args[1].isnumeric():
                limitrows = int(context.args[1])
        elif (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /node tên_node")
            return
        nodesearch = nodes_select2(context.args[0], limitrows)
        l = len(nodesearch)
        if l == 1:
            result = node_detail(str(nodesearch[0]['Nodename']))
            update.message.reply_text("Node details: \n" 
                                      + json.dumps(result, indent = 1, ensure_ascii=False).replace('"',''))    
        elif l > 1:
            nodesearch=json.dumps(nodesearch, indent = 1, ensure_ascii=False)
            update.message.reply_text("Vị trí node: \n" + nodesearch.replace('"','')
                                      + "\nĐể biết chi tiết thiết bị của node bạn cần chính xác tên node"
                                      )
        else:
            update.message.reply_text("Không tìm thấy node bạn yêu cầu")
    except Exception as e:
        print(e)

def node_detail(nodename):
    try:
        conn = connect()
        db_df = pd.read_sql_query("SELECT n.name as TênNode, n.onmip as IP, eq.name as TênTBC, ch.name as TênChassis, co.name as trênRack, ch.position as tạiU FROM equipment eq "
                       + "left join nodes n on n.id=eq.node_id "
                       + "left join chassis ch on ch.id=eq.chassis_id "
                       + "left join containers co on co.id=ch.container_id "
                       + "WHERE n.node_status_id<7 and n.name like '" + nodename + "'"
                       , conn)
        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return data
    except Exception as e:
        print(e)
    finally:
        conn.close()

#========================================
def note_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /note is issued."""
    debug_log(update)
    try:
        if not hasattr(update.message.reply_to_message, "text"):
            update.message.reply_text("Để ghi chú vào log kiểm kê: reply tin_nhắn_cần_ghi_chú, soạn: /note nội_dung_ghi_chú")
            return
        assetschecklog(update.message.chat.id,update.message.reply_to_message.text,update.message.text)
        update.message.reply_text("Đã cập nhật ghi chú cho:" + update.message.reply_to_message.text 
                                  + ", nội dung:" + update.message.text)
    except Exception as e:
        print(e)
        
#=========================================
def user_command(update: Update, context: CallbackContext) -> None:
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    """Send a message when the command /user is issued."""
    debug_log(update)
    try:
        conn = sqlite3.connect(db_file)
        db_df = pd.read_sql_query("SELECT *, datetime(time,'localtime') FROM config", conn)
        db_df.to_excel(log_path + "config.xlsx", index=False)
        document = open(log_path + "config.xlsx", 'rb')
        update.message.reply_document(document=document)
    except Exception as e:
        print(e)

#=================================================
def nhap_command(update: Update, context: CallbackContext) -> None:
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    """Send a message when the command /nhap is issued."""
    print("nhap_command:")
    debug_log(update)
    limitrows = 5
    try:
        if (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /nhap serial")
            return
        update.message.reply_text("Bạn nhập kho tài sản sau: " + context.args[0])
        result = assets_check(context.args[0], limitrows)
        update.message.reply_text(result.replace('"',''))
        data1={
            "command":"Nhap",
            "data":update.message.text
            }
        data2={
            "command":"Cancel",
            "data":""
            }
        print(data1)
        print(data2)
        keyboard = [
            [
                InlineKeyboardButton("Xác nhận", callback_data=json.dumps(data1)),
                InlineKeyboardButton("Hủy", callback_data=json.dumps(data2)),
            ],
        
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Vui lòng xác nhận nhập kho:', reply_markup=reply_markup)
    except Exception as e:
        print(e)

#================================================
def xuat_command(update: Update, context: CallbackContext) -> None:
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    """Send a message when the command /xuat is issued."""
    print("xuat_command:")
    debug_log(update)
    limitrows = 5
    try:
        if (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /xuat serial")
            return
        update.message.reply_text("Bạn xuất kho tài sản sau: " + context.args[0])
        result = assets_check(context.args[0], limitrows)
        update.message.reply_text(result.replace('"',''))
    
        data1={
            "command":"Xuat",
            "data":update.message.text
            }
        data2={
            "command":"Cancel",
            "data":""
            }
        print(data1)
        print(data2)
        keyboard = [
            [
                InlineKeyboardButton("Xác nhận", callback_data=json.dumps(data1)),
                InlineKeyboardButton("Hủy", callback_data=json.dumps(data2)),
            ],
        
        ]
        
        
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Vui lòng xác nhận xuất kho:', reply_markup=reply_markup)
    except Exception as e:
        print(e)

#====================================================
def button(update: Update, context: CallbackContext) -> None:
    print("button:")
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    #print(query.message)
    query.answer()
    query.edit_message_text(text=query.message.text + f"{query.from_user.first_name} {query.from_user.last_name} đã xác nhận: {query.data}")
    
    """    
    if query.data =='0':
        return
    if query.data =='updated' or query.data =='no_change':
        return
    else:
        warehouse_log(datatuple)
    """
    print(query.data)
    data=json.loads(query.data)
    #print(type(data))
    command=data['command']    
    
    print("command:")

    if command=='Cancel':
        print(command)
        print(data["data"])
        return
    elif command=='Xuat' or command=='Nhap':
        print(command)
        #datatuple=(chatid, firstname, lastname, data)
        datatuple=(query.from_user.id, query.from_user.first_name, query.from_user.last_name, data["data"])
        print(json.dumps(datatuple, indent = 1, ensure_ascii=False))
        warehouse_log(datatuple)
    elif command=="updated" or command=="no_change":
        print(command)
        print(data["data"])
        return
    elif command=="Aprove":
        print(command)
        print(data["data"])  
        chatid=data["data"]["chatid"]
        register(chatid,0)
        context.bot.send_message(chat_id=chatid
                             ,text="Admin đã phê duyệt yêu cầu đăng nhập của bạn"
                             ) 
        return
    elif command=="Temp2h":
        print(command)
        print(data["data"])
        chatid=data["data"]["chatid"]
        register(chatid,2)
        context.bot.send_message(chat_id=chatid
                             ,text="Admin đã phê duyệt, bạn được đăng nhập trong vòng 2h"
                             ) 
        return
    elif command=="Reject":
        print(command)
        print(data["data"])
        chatid=data["data"]["chatid"]
        context.bot.send_message(chat_id=chatid
                             ,text="Admin đã từ chối yêu cầu đăng nhập của bạn"
                             ) 
        return
    else:
        print(f"else: {command}")
        print(data["data"])
        return


def warehouse_log(datatuple):
    """ Connect to SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        #insert warehouselog
        insert_log_sql = """INSERT INTO warehouselog (chatid, firstname, lastname, data) VALUES (?,?,?,?)"""
        #datatuple=(chatid, firstname, lastname, data)
        c.execute(insert_log_sql,datatuple)
        conn.commit()
    except sqlite3.Error as e:
        print(e)
        #create table
        create_table_sql = """CREATE TABLE IF NOT EXISTS warehouselog
                 (id INTEGER PRIMARY KEY,
                  time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  chatid varchar(20) NOT NULL,
                  firstname text,
                  lastname text,
                  data text,
                  serial text,
                  result text,
                  note text)"""
        c.execute(create_table_sql)    
    finally:
        if (conn):
            conn.close()

#=========================================
def getlogwh_command(update: Update, context: CallbackContext) -> None:
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    """Send a message when the command /getlogwh is issued."""
    debug_log(update)
    try:
        conn = sqlite3.connect(db_file)
        db_df = pd.read_sql_query("SELECT *, datetime(time,'localtime') FROM warehouselog", conn)
        db_df.to_excel(log_path + "warehouselog.xlsx", index=False)
        document = open(log_path + "warehouselog.xlsx", 'rb')
        update.message.reply_document(document=document)
    except Exception as e:
        print(e)

#============================================
import requests

#proxy http
http_proxy  = "http://192.168.0.99:8081"
https_proxy = "https://192.168.0.99:8081"
proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy
              }
#web services account
user="tthht"
    
def sms_command(update: Update, context: CallbackContext) -> None:
    debug_log(update)
    phone=context.args[0]
    message=update.message.text

    url="http://192.168.53.29:8000/Service1.asmx?op=SendMT"
    headers = {'content-type': 'text/xml'}
    body = f"""<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
              <soap:Body>
                <SendMT xmlns="http://tempuri.org/">
                  <userName>{user}</userName>
                  <phoneNumber>{phone}</phoneNumber>
                  <message>{message}</message>
                </SendMT>
              </soap:Body>
            </soap:Envelope>"""
    try:
        response = requests.post(url,data=body,headers=headers, proxies=proxyDict)
        print(response.content)
    except Exception as e:
        print(e)

#===========================================
def getlogac_command(update: Update, context: CallbackContext) -> None:
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    """Send a message when the command /ac is issued."""
    debug_log(update)
    try:
        if(connectbms()):
            conn = connectbms()
        else:
            return False
        db_df = pd.read_sql_query("SELECT ACEInstance, EventTime, EventObjectName, CardUserName, CardUserNumber FROM acevent "
                                   + "WHERE CardUserNumber <> 0 and date(EventTime)>=(NOW() - INTERVAL 1 DAY) "
                                  , conn)
        db_df.to_excel(log_path + "aclog.xlsx", index=False)
        document = open(log_path + "aclog.xlsx", 'rb')
        update.message.reply_text("Log access control trong 24h qua:")
        update.message.reply_document(document=document)
    except Exception as e:
        print(e)

#=============================================
def acs_job(context: CallbackContext) -> None:
    print('acs_job start')
    try:
        result = acslog()
        if len(result)>0:
            #context.bot.send_message(chat_id=GroupId, text="Log ra vào kho 1h qua:")
            text=json.dumps(result, indent = 1, ensure_ascii=False)
            message=context.bot.send_message(chat_id=GroupId, text="Log ra vào kho 1h qua:" + text.replace('"',''))
            print("msg id of log ra vao kho:")
            msg_id=message.message_id
            print(msg_id)
            reminder(context, msg_id)
        else:
            print("no acess control log")
    except Exception as e:
        print(e)

def logconfirm(context):
    #https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
    logging.info("schedule run_once:")
    print("logconfirm:")
    data=context.job.context
    print(data) 
    data1={
        "command":"updated",
        "data":"update_later"
        }
    data2={
        "command":"no_change",
        "data":"no_change"
        }
    print(data1)
    print(data2)
    keyboard = [
                [
                    InlineKeyboardButton("Tôi sẽ cập nhật sau", callback_data=json.dumps(data1)),
                    InlineKeyboardButton("Không xuất/nhập thực", callback_data=json.dumps(data2)),
                ],
                ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
       
    #if exist(log) data['Door'] send message
    #translate data['Name'] to chatid   
    print(data["msg_id"])
    print(type(data["msg_id"]))
    context.bot.send_message(chat_id=GroupId
                             ,text=f"Log ghi sổ xuất/nhập kho 4h qua như trên(xem /logwh). Đề nghị @{data['Name']} xác nhận biến động kho {data['Door']}:"
                             ,reply_to_message_id=data["msg_id"] 
                             ,reply_markup=reply_markup)


def logxuatnhap(context):
    #https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
    logging.info("schedule run_once:")
    print("logxuatnhap:")
    msg_id=context.job.context
    print(msg_id)
    
    #getlog all warehouse in 4 hours
    try:
        conn = sqlite3.connect(db_file)
        db_df = pd.read_sql_query("SELECT *, datetime(time,'localtime') FROM warehouselog "
                                  +" WHERE datetime(time) >=datetime('now', '-4 Hour') "
                                  , conn)
        #Note Sql syntax
        #Sqlite: datetime(time) >=datetime('now', '-4 Hour')
        #mySql:  time >=(NOW()-INTERVAL 4 HOUR)
        if db_df.id.count()==0:
            context.bot.send_message(chat_id=GroupId
                                     , text=f"Log ghi sổ xuất/nhập kho 4h qua, có: {str(db_df.id.count())} biến động."
                                     +" Để ghi sổ /xuat serial hoặc /nhap serial , để xem /logwh"
                                     , reply_to_message_id=msg_id
                                     )
        else:    
            db_df.to_excel(log_path + "warehouselog.xlsx", index=False)
            document = open(log_path + "warehouselog.xlsx", 'rb')      
            context.bot.send_document(chat_id=GroupId
                                      ,caption=f"Log ghi sổ xuất/nhập kho 4h qua, có: {str(db_df.id.count())} biến động."
                                       +" Để ghi sổ /xuat serial hoặc /nhap serial , để xem /logwh"
                                      , reply_to_message_id=msg_id
                                      , document=document)
    except Exception as e:
        print(e)



def reminder(context: CallbackContext,msg_id):
    print("reminder function:")
    data = acscount()
    context.job_queue.run_once(logxuatnhap,when=10740,name="logXuatNhap4h", context=msg_id)
    for x in range(len(data)):
        data[x]["msg_id"]=msg_id
        print(data[x])
        print(type(data[x]))
        context.job_queue.run_once(logconfirm,when=10800,name=f"reminder_{data[x]['Name']}_{data[x]['Door']}", context=data[x])
        #context.job_queue.run_once(logconfirm,when=30,name=f"reminder_{data[x]['Name']}_{data[x]['Door']}", context=data[x])


def acslog():
    try:
        if(connectbms()):
            conn = connectbms()
        else:
            return False
        db_df = pd.read_sql_query("SELECT ACEInstance as Id, EventTime as Time, EventObjectName as Door, CardUserName as Name, CardUserNumber as UserId FROM acevent "
                       + "WHERE CardUserNumber <> 0 and EventTime>=(NOW() - INTERVAL 1 HOUR) "
                       + "and (EventObjectName like '%T3_Phong NOC%' or EventObjectName like '%Hanh lang 2%')"
                      , conn)
        #print(db_df)
        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return data
    except Exception as e:
        print(e)
    finally:
        conn.close()

def acscount():
    try:
        if(connectbms()):
            conn = connectbms()
        else:
            return False
        db_df = pd.read_sql_query("SELECT ACEInstance as Id, EventTime as Time, EventObjectName as Door, CardUserName as Name, CardUserNumber as UserId FROM acevent "
                       + "WHERE CardUserNumber <> 0 and EventTime>=(NOW() - INTERVAL 1 HOUR) "
                       + "and (EventObjectName like '%T3_Phong NOC%' or EventObjectName like '%Hanh lang 2%') "
                       + " group by Door, Name"
                      , conn)
        #print(db_df)
        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return data
    except Exception as e:
        print(e)
    finally:
        conn.close()
#==================================================
def schedule_job(context: CallbackContext) -> None:
    print('getlog job start')
    result = getcsvlog()
    if result=='0':
        print("không có Log tài sản 4h qua trên pmTTTM")
        return False
    try:
        #context.bot.send_message(chat_id=GroupId, text="Log tài sản 4h qua trên pmTTTM, có: " + result 
        #                         + " biến động. Chi tiết theo file đính kèm")
        document = open(log_path + "assests_log.xlsx", 'rb')
        context.bot.send_document(chat_id=GroupId
                                  , caption=f"Log tài sản 4h qua trên pmTTTM, có: {result} biến động." 
                                 + " Chi tiết theo file đính kèm"
                                  , document=document)
    except Exception as e:
        print(e)

def getcsvlog():
    try:
        conn = connect()                              
        db_df = pd.read_sql_query("SELECT a.id, a.serial, al.content as Nộidung, wh1.name as KhoĐi, wh2.name as KhoĐến "
                           + "FROM asset_logs al left join assets a on a.id=al.asset_id "
                           + "left join warehouses wh1 on al.from_warehouse=wh1.id "
                           + "left join warehouses wh2 on al.to_warehouse=wh2.id "
                           + "WHERE al.updated_at>=(NOW() - INTERVAL 4 HOUR)", conn)
        db_df.to_excel(log_path + "assests_log.xlsx", index=False)
        return str(db_df.id.count())
    except Exception as e:
        print(e)

#=============================================
def addjob_command(update: Update, context: CallbackContext) -> None:
    debug_log(update)
    try:
        update.message.reply_text("A test job name <addjobtest> was added, it wil run in 30s. "
                                  +"check /job to list job in queue")
        context.job_queue.run_once(test,when=30,name="addjobtest",context=update)
    except Exception as e:
        print(e)

def test(context):
    #https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
    logging.info("schedule run_once:")
    print("test job")
    update=context.job.context
    #print(update)
    data1={
        "command":"updated",
        "data":"updated"
        }
    data2={
        "command":"no_change",
        "data":"no_change"
        }
    print(data1)
    print(data2)
    keyboard = [
                [
                    InlineKeyboardButton("Tôi sẽ cập nhật sau", callback_data=json.dumps(data1)),
                    InlineKeyboardButton("Không xuất/nhập thực", callback_data=json.dumps(data2)),
                ],
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.message.chat.id, text='Xác nhận test:', reply_markup=reply_markup)

#================================================
def job_command(update: Update, context: CallbackContext) -> None:
    debug_log(update)
    update.message.reply_text("list job in queue:")
    remove_job_if_exists(update, context)

def remove_job_if_exists(update,context):
    """Remove job with given name. Returns whether job was removed."""
    all_jobs = context.job_queue.jobs()
    if not all_jobs:
        return False
    for job in all_jobs:
        print(job.name)
        update.message.reply_text(job.name)
        #to run job
        #job.run(context.dispatcher)
        if (len(context.args))>0:
            if context.args[0]=='r':
                #to remove job
                job.schedule_removal()
    return True

#===================================================
def bms_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /bms is issued."""
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    try:
        myinput=pd.read_excel(log_path + 'input.xlsx')
        myinput=myinput.Name.to_list()
        #print(type(myinput))
        #print(myinput)
        listpoint=[]
        for item in myinput:
            result=getbms(item)
            listpoint.append(result)
        df=pd.DataFrame(listpoint,columns=['Name','Data','Timestamp','Delay'])
        #print(df)
        df.to_excel(log_path + "result.xlsx", index=False)
        document = open(log_path + "result.xlsx", 'rb')
        update.message.reply_text("BMS report:")
        update.message.reply_document(document=document)        
    except Exception as e:
        print(e)

import datetime;
import dateutil.parser as tp

def getbms(pattern):
    limitrows = 5
    try:
        bmspoint = bms_point(pattern, limitrows)
        """
        for item in bmspoint:
            bmsvalue=bms_value(item['TLInstance'],item['RecordCount'])
            a=(item['Name'])
            b=(bmsvalue[0]['Data'])
            c=(bmsvalue[0]['Timestamp'])  
        """
        if len(bmspoint)>1:
            a=pattern
            b="multiplepoint, check the Name"
            c="N/A"
            d=""
        elif len(bmspoint)==1:
            bmsvalue=bms_value(bmspoint[0]['TLInstance'],bmspoint[0]['RecordCount'])
            a=(bmspoint[0]['Name'])
            b=(bmsvalue[0]['Data'])
            c=(bmsvalue[0]['Timestamp']) 
            ts1 = datetime.datetime.now().timestamp()+7*60*60
            ts2 = tp.parse(c).timestamp()           
            d=(str(round((ts1-ts2)/(60),0)) + " minute ago")
        else:
            a=pattern
            b="dont exist, check the Name"
            c="N/A"
            d=""
        return [a,b,c,d]
    except Exception as e:
        print(e)

def bms_value(TLInstance, RecordCount):
    try:
        if(connectbms()):
            conn = connectbms()
        else:
            return False
        db_df = pd.read_sql_query(f"select * from tldata where RecordNumber={RecordCount} and TLInstance={TLInstance}"
                          , conn)
        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return data
        #return json.dumps(data, indent = 1, ensure_ascii=False)
    except Exception as e:
        print(e)
    finally:
        conn.close()

def bms_point(point, limitrows):
    try:
        if(connectbms()):
            conn = connectbms()
        else:
            return False
        point = point.replace("%","\%");
        point = point.replace("_","\_");
        db_df = pd.read_sql_query(f"select Name, TLInstance, RecordCount from tl where NAME LIKE '{point}' limit {limitrows}"
                      , conn)
        result=db_df.to_json(orient="records", date_format='iso')
        data = json.loads(result)
        return data
    except Exception as e:
        print(e)
    finally:
        conn.close()

#===================================================

def fiber_command(update: Update, context: CallbackContext) -> None:
    
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    try:
        if (len(context.args))==0:
            update.message.reply_text("Cấu trúc lệnh như sau: /fiberscan swname")
            return
        sw = context.args[0]
        
        sys.path.insert(1, 'D:/minhnt27/chatbot/')
        from rx_scanner import rxscan
        rxscan(sw)
        print(f"arg:{sw}")
        df = rxpower(sw)
        df.to_excel(log_path + "fiber.xlsx", index=False)
        document = open(log_path + "fiber.xlsx", 'rb')
        update.message.reply_text("Fiber report:")
        update.message.reply_document(document=document)        
    except Exception as e:
        print(e)


db_name2='autotester'
def connect2():
    try:
        conn = mysql.connector.connect(host=host_ip,database=db_name2,user='tableau', password='Tthht@123')
        #if conn.is_connected():
        #    print('Connected to MySQL database\n')
    except mysql.Error as e:
        print(e)
    finally:
        return conn

def rxpower(sw):
    print("rxpower function works")
    try:
        
        conn = connect2()
        db_df = pd.read_sql_query("select se.swname, cf.port, round(rp.rx_power- rp.threshold,1) AS state,"
                                  +"rp.rx_power, rp.tx_power, rp.threshold, rp.update_at "
                                  +"from rx_power rp "
                                  +"left join config cf on rp.if_id=cf.id "
                                  +"left join session se on cf.session_id=se.id  "
                                  +f"where se.swname like '{sw}' and "
                                  +"rp.id IN (select max(id) from rx_power where update_at>=(NOW()-INTERVAL 1 DAY) group by if_id )"
                                  , conn)
        #result=db_df.to_json(orient="records", date_format='iso')
        #data = json.loads(result)
        return db_df
    except Exception as e:
        print(e)
    finally:
        conn.close()
      
#===================================================
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    debug_log(update)
    update.message.reply_text("Cấu trúc command: /command arg0 arg1 ...với arg là tham số đầu vào đầu tiên, "
                              + "cách nhau bằng khoảng trắng, không phân biệt ký tự hoa/thường. "
                              + "Hệ thống hỗ trợ các tác vụ sau:"
                              +'\n/help :Giúp đỡ, không tham số'
                              +'\n/who :Giới thiệu bot chat, không tham số'
                              +"\n/where :Xác định vị trí node mạng, tham số arg0 chứa tên node, vd:/where S6405, "
                              + "kết quả trả về tối đa 5. Khi tên node chính xác sẽ trả về vị trí các rack"
                              +"\n/serial :Xác định vị trí của tài sản, tham số arg0 chứa serial, vd:/serial K926, "
                              + "kết quả trả về tối đa 5"
                              +"\n/sparetb :Xác định vật tư dự phòng BanTB, tham số arg0 chứa Mã/tên VHKT, vd:/spare scu, "
                              + "kết quả trả về tối đa 5"
                              +"\n/sparetd :Xác định vật tư dự phòng BanTD, tham số arg0 chứa Mã/tên VHKT, vd:/spare sio, "
                              + "kết quả trả về tối đa 5"
                              +"\n/node :Cung cấp chi tiết IP Node, các thiết bị con, các chassis, "
                              + "chú ý tham số arg0 phải chứa chính xác tên Node, vd:/node iMHT04. "
                              +"\nClick /more để thêm các lệnh"
                              )
    updateuser(update.message.chat.id, update.message.chat.first_name, update.message.chat.last_name)

def more_command(update: Update, context: CallbackContext) -> None:
    debug_log(update)
    update.message.reply_text("/getlog :Cho phép download log file excel kiểm kê tài sản"
                              +"\n/dellog :Cho phép xóa log kiểm kê tài sản"
                              +"\n/note :Cho phép ghi chú khi kiểm kê tài sản, bằng cách reply đoạn text cần ghi chú và nhập /note <nội dung ghi chú>"
                              +"\nKiểm kê tài sản: các chuỗi không bắt đầu bằng / không phải là command và hệ thống sẽ xử lý kiểm kê như là "
                              + "1 serial. Để dùng máy bắn serial, vào settings Telegram/Chat Settings/Send by Enter bật lên "
                              +"\n/audit : Thiết lập node để lấy log audit. Thiết lập mới sẽ xóa toàn bộ log audit cũ"
                              +"\n/auditlog : Lấy file kết quả audit của node đã thiết lập"
                              +"\n/xuat : xuất kho card UCTT, vd: /xuat 123456789"
                              +"\n/nhap : nhập kho card UCTT, vd: /nhap 123456789 kệ5"
                              +"\n/logwh : Lấy file kết quả xuất nhập kho UCTT"
                              )
    #updateuser(update.message.chat.id, update.message.chat.first_name, update.message.chat.last_name)

def more2_command(update: Update, context: CallbackContext) -> None:
    if not(login(update.message.chat.id)):
        update.message.reply_text('Chào bạn! Đây là chatbot của TTr.HHT, để sử dụng bạn gõ /grant để yêu cầu đăng nhập, sau khi Admin aprove sẽ có tin nhắn xác nhận')
        return
    debug_log(update)
    update.message.reply_text("/sms :sms <phonenumber without 0> <message>"
                              +"\n/job :list jobs in schedule"
                              +"\n/addj :add test jobs in schedule"
                              +"\n/ac :log access control 24h"
                              +"\n/bms :bms info"
                              +"\n/fiberscan swname: rx of sw info"
                              +"\n/grant :request Admin to grant login right"
                              +"\n/revoke :to kickout user"
                             )

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    try:
        updater = Updater(TOKEN, use_context=True)
        
        #Request._request_wrapper(headers="abc")

        # schedule job
        job = updater.job_queue
        job.run_repeating(schedule_job, interval=14400, first=60)
        job.run_repeating(acs_job, interval=3600, first=90)
        #job.run_repeating(schedule_job, interval=86400, first=0,name="minhnt27")
        #job.run_daily(schedule_job,time = time(hour = 23, minute = 0, second = 0),days=(0, 1, 2, 3, 4, 5, 6))

        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("who", who_command))
        dispatcher.add_handler(CommandHandler("where", where_command))
        dispatcher.add_handler(CommandHandler("w", where_command))
        dispatcher.add_handler(CommandHandler("serial", serial_command))
        dispatcher.add_handler(CommandHandler("sparetb", spare_command))
        dispatcher.add_handler(CommandHandler("sparetd", sparetd_command))
        dispatcher.add_handler(CommandHandler("node", node_command))
        dispatcher.add_handler(CommandHandler("getlog", getlog_command))
        dispatcher.add_handler(CommandHandler("dellog", dellog_command))
        
        dispatcher.add_handler(CommandHandler("more", more_command))
        dispatcher.add_handler(CommandHandler("note", note_command))
        dispatcher.add_handler(CommandHandler("audit", audit_command))
        dispatcher.add_handler(CommandHandler("auditlog", getaudit_command))
        dispatcher.add_handler(CommandHandler("user", user_command))
        dispatcher.add_handler(CommandHandler("nhap", nhap_command))
        dispatcher.add_handler(CommandHandler("xuat", xuat_command))
        dispatcher.add_handler(CommandHandler("logwh", getlogwh_command))
        
        dispatcher.add_handler(CommandHandler("more2", more2_command))
        dispatcher.add_handler(CommandHandler("sms", sms_command))
        dispatcher.add_handler(CommandHandler("job", job_command))
        dispatcher.add_handler(CommandHandler("ac", getlogac_command))
        dispatcher.add_handler(CommandHandler("addj", addjob_command))
        dispatcher.add_handler(CommandHandler("bms", bms_command))
        dispatcher.add_handler(CommandHandler("fiberscan", fiber_command))
        
        dispatcher.add_handler(CommandHandler("grant", grant_command))
        dispatcher.add_handler(CommandHandler("revoke", revoke_command))
        
        # on button click -                          
        dispatcher.add_handler(CallbackQueryHandler(button))

        # on noncommand i.e message - echo the message on Telegram
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check))

        # Start the Bot
        updater.start_polling()

        # Run the bot until you press Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()