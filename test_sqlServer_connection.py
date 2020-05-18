import pyodbc 
# For test connection
server = '192.168.1.1'
port = '1433'
database = 'abc' 
username = 'abc' 
password = '******' 

conString = 'DRIVER={SQL Server};SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+ password
#print(conString)
#try other driver if eror: {SQL Server Native Client 11.0}, {ODBC Driver 17 for SQL Server}
cnxn = pyodbc.connect(conString)
#cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

#Sample select query
cursor.execute("SELECT @@version;") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()