#Before running the program to test, you need to install Azure SQL drivers
#Link to download: https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15

import pyodbc
server = 'physicalsecuritydb.database.windows.net'
database = 'physical-security-db'
username = 'database_user'
password = '{Password123}'   
driver= '{ODBC Driver 17 for SQL Server}'
conn=pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor=conn.cursor()

#Instruction: Use cursor.execute('Command') to run commands. use cursor.fetchone() to fetch output
#Instruction: Remove the word pass from the methods after adding the commands

#References: https://docs.microsoft.com/en-us/azure/azure-sql/database/connect-query-python



def createTable():
	cursor.execute("CREATE TABLE [User](username VARCHAR(30) NOT NULL UNIQUE, device_id VARCHAR(10) NOT NULL UNIQUE,email VARCHAR(30) NOT NULL UNIQUE)")
	cursor.commit()
	#TODO Create table with columns username, device_id, email. All device_id is VARCHAR(10), others are VARCHAR(30)
	#All are NOT NULL and UNIQUE
	
	
def addUser(username, device_id, email):
	
	command = 'INSERT INTO [User] VALUES (?,?,?)'
	
	cursor.execute(command,username,device_id,email)
	cursor.commit()
	#TODO add the user to table
	
	
def getEmailFromUser(username):
	command ='SELECT email FROM [User] WHERE username=?'
	cursor.execute(command,username)
	cursor.commit()
	retValue=cursor.fetchall()
	return retValue
	#TODO return email of the user by searching with username 
	
	
def getDeviceFromUser(username):
	command='SELECT device_id FROM [User] WHERE username=?'
	
	cursor.execute(command,username)
	cursor.commit()
	retValue=cursor.fetchall()
	return retValue
	#TODO return device id of the user by searching with username

addUser("{username}","{device_id}","{email}")
getEmailFromUser("{username}")
getDeviceFromUser("{username}")

