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
	#TODO Create table with columns username, device_id, email. All device_id is VARCHAR(10), others are VARCHAR(30)
	#All are NOT NULL and UNIQUE
	pass
	
def addUser(username, device_id, email):
	#TODO add the user to table
	pass
	
def getEmailFromUser(username):
	#TODO return email of the user by searching with username 
	pass
	
def getDeviceFromUser(username):
	#TODO return device id of the user by searching with username 
	pass
	
