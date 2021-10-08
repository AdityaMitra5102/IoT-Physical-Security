

import pyodbc
server = 'physicalsecuritydb.database.windows.net'
database = 'physical-security-db'
username = 'database_user'
password = '{Password123}'   
driver= '{ODBC Driver 17 for SQL Server}'
conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor=conn.cursor()





def createTable():
	try:
		cursor.execute("CREATE TABLE [User](username VARCHAR(30) NOT NULL UNIQUE, device_id VARCHAR(10) NOT NULL UNIQUE,email VARCHAR(30) NOT NULL )")
		cursor.commit()
	except:
		pass
	
	
def addUser(username, device_id, email):
	command = 'INSERT INTO [User] VALUES (?,?,?)'	
	cursor.execute(command,username,device_id,email)
	cursor.commit()
	
	
	
def getEmailFromUser(username):
	try:
		command ='SELECT email FROM [User] WHERE username=?'
		cursor.execute(command,username)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
		 
	except:
		return "00"
	
def getDeviceFromUser(username):
	try:
		command='SELECT device_id FROM [User] WHERE username=?'
		cursor.execute(command,username)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
		
	except:
		return "00"
		
def getUserFromDevice(device_id):
	try:
		command='SELECT username FROM [User] WHERE device_id=?'
		cursor.execute(command,device_id)
		retValue=cursor.fetchone()[0]
		cursor.commit()
		return retValue
	
	except:
		return "00"
		
def deleteFromUser(username):
	command='DELETE FROM [User] WHERE username=?'
	cursor.execute(command,username)
	cursor.commit()

def dropTable():
	cursor.execute("DROP TABLE IF EXISTS [User]")
	cursor.commit()
		
def resetDb():
	dropTable()
	createTable()
		
	
