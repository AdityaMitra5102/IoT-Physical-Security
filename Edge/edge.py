from flask import Flask, session, request, redirect, abort
import os
import pyqrcode
import png
from pyqrcode import QRCode
import string
import random
from crypto import *

app = Flask(__name__, static_url_path="")
id=''
token=''
server="https://cryptane:5000"

@app.route('/')
def index():
	global server
	url=server+"/checkfirsttime?id="
	idencr=encrypt(id,key5)
	url+=idencr
	return redirect(url)

    
@app.route('/startunlock')
def startunlock():
	global token
	global server
	url=server+"/unlockinit?id="
	idencr=encrypt(id,key2)
	url+=idencr
	url+="&auth="
	token=makeId()
	enctoken=encrypt(token,key3)
	url+=enctoken
	return redirect(url)
	
@app.route('/unlockdone',methods=['GET'])
def unlockdone():
	global token
	print(token)
	cipher=request.args.get('id')
	temp=decrypt(cipher,key4)
	#print(temp)
	print(token)
	if temp==token:
		print("Unlocked")
		serialoutput()  
	return redirect("/")  
    
@app.route('/qrcode')
def qrcode():
	global server
	url=server+"/devicereg?id="
	idencr=encrypt(id,key1)
	url+=idencr
	q=pyqrcode.create(url)
	print(url)
	q.png('./static/regqr.png',scale=6)
	return redirect("/qrcodereg.html")


def getId():
	global id
	if not os.path.exists(".deviceid.pkl"):
		id=makeId()
		idencr=encrypt(id,key0)
		f=open(".deviceid.pkl","w+")
		f.write(idencr)
		f.close()
	else:
		f=open(".deviceid.pkl", "r")
		idcipher=f.read()
		f.close()
		id=decrypt(idcipher,key0)
		print(id)
		
def makeId():
	characters = string.ascii_letters + string.digits
	password = ''.join(random.choice(characters) for i in range(10))
	return password

def serialoutput():
	pass
	
if __name__ == '__main__':
    getId()
    app.run(port=8080)