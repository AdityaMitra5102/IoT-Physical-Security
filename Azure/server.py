from __future__ import print_function, absolute_import, unicode_literals
from fido2.webauthn import PublicKeyCredentialRpEntity
from fido2.client import ClientData
from fido2.server import Fido2Server
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2 import cbor
from flask import Flask, session, request, redirect, abort
from crypto import *
from sqltasks import *
from otp import *
import pickle
import os


app = Flask(__name__, static_url_path="")
app.secret_key = os.urandom(32)  # Used for session.

rp = PublicKeyCredentialRpEntity("cryptane", "Demo server")
server = Fido2Server(rp)
user='user1'
email=''
uname=''
otp=''
credentials = []
devtemp=''
operation=1 #1=signup, 2=login
authtoken=''


@app.route("/")
def index():
    global email
    global uname
    global user
    email=''
    uname=''
    user=''
    return redirect("/index.html")

@app.route("/resetdb") #Only for testing
def resetdatabase():
	resetDb()
	return ("Database reset")
	    
@app.route("/unlockinit", methods=["GET"])
def unlockinit():
	global user
	global authtoken
	cipher1=request.args.get('id')
	cipher2=request.args.get('auth')
	print(cipher1)
	print(cipher2)
	user=decrypt(cipher1,key2)
	print(user)
	authtoken=decrypt(cipher2,key3)
	print(authtoken)
	return redirect("/authenticatefido.html")

@app.route("/checkfirsttime", methods=["GET"])
def checkfirsttime():
	cipher=request.args.get('id')
	temp=decrypt(cipher,key5)
	u=getUserFromDevice(temp)
	if u=="00":
		return redirect("http://localhost:8080/qrcode")
	return redirect("http://localhost:8080/unlockmenu.html")
	
@app.route("/unlocksuccess")
def unlocksuccess():
	global authtoken
	token=encrypt(authtoken,key4)
	return redirect("http://localhost:8080/unlockdone?id="+token)
	
@app.route("/loginresp", methods=["POST"])
def loginresp():
	global email
	global uname
	global operation
	operation=2
	uname=request.form['uname']
	try:
		email=getEmailFromUser(uname)
		print(email)
		print(uname)
		operation=2
		sendOTP()
		return redirect("/otp.html")
	except:
		return redirect("/badlogin.html")


@app.route("/deleteallkeys")
def deleteallkeys():
	filename=user+'datafilekey.pkl'
	if os.path.exists(filename):
		os.remove(filename)
	return redirect("/home.html")

@app.route("/devicereg", methods=["GET"])
def devicereg():
	global devtemp
	cipher=request.args.get('id')
	devtemp=decrypt(cipher,key1)
	return redirect("/signup.html")
	
@app.route("/signupresp", methods=["POST"])
def signupresp():
	global email
	global uname
	global operation
	email=request.form['email']
	uname=request.form['username']
	print(email)
	print(uname)
	operation=1
	sendOTP()
	return redirect("/otp.html")

@app.route("/otpauth", methods=["POST"])
def otpauth():
	global otp
	global uname
	global devtemp
	global email
	global user
	recotp=request.form['cred']
	if (recotp==otp):
		print('Auth successful')
		if operation==1:
			user=devtemp
			try:
				addUser(uname,user,email)
			except:
				return redirect("/userexists.html")
		return redirect("/home.html")
	otp=''
	return redirect("/badotp.html")

@app.route("/api/register/beginkey", methods=["POST"])
def register_beginkey():
    global user
    credentials=readkey()
    #regdict=read1()
    uid=user+"fido"
    registration_data, state = server.register_begin(
        {
            "id": uid.encode('ascii'),
            "name": "a_user",
            "displayName": "A. User",
            "icon": "https://example.com/image.png",
        },
        credentials,
        user_verification="discouraged",
        authenticator_attachment="cross-platform",
    )

    session["state"] = state
    print("\n\n\n\n")
    print(registration_data)
    #regdata.append(user)
    print("\n\n\n\n")
    return cbor.encode(registration_data)


@app.route("/api/register/completekey", methods=["POST"])
def register_completekey():
    credentials=readkey()
    #regdict=read1()
    data = cbor.decode(request.get_data())
    client_data = ClientData(data["clientDataJSON"])
    #print(client_data)
    att_obj = AttestationObject(data["attestationObject"])
    #print("clientData", client_data)
    #print("AttestationObject:", att_obj)

    auth_data = server.register_complete(session["state"], client_data, att_obj)
    #print(auth_data)
    credentials.append(auth_data.credential_data)
    print("REG DONE")
    savekey(credentials)
    l=str(auth_data.credential_data)
    print(data)
    l=l[l.index('credential_id'):l.index('public_key')-2]
    return cbor.encode({"status": "OK"})


@app.route("/api/authenticate/beginkey", methods=["POST"])
def authenticate_beginkey():
    credentials=readkey()
    if not credentials:
        abort(404)
    auth_data, state = server.authenticate_begin(credentials)
    session["state"] = state
    return cbor.encode(auth_data)


@app.route("/api/authenticate/completekey", methods=["POST"])
def authenticate_completekey():
    global user
    credentials=readkey()
    if not credentials:
        abort(404)

    data = cbor.decode(request.get_data())
    credential_id = data["credentialId"]
    client_data = ClientData(data["clientDataJSON"])
    auth_data = AuthenticatorData(data["authenticatorData"])
    signature = data["signature"]
    print(data)
    cred=server.authenticate_complete(
        session.pop("state"),
        credentials,
        credential_id,
        client_data,
        auth_data,
        signature,
    )
    print("ASSERTION OK")
    print("Authenticated "+user);
    return cbor.encode({"status": user})
    
def savekey(credentials):
	global user
	with open(user+'datafilekey.pkl','wb') as outp1:
		pickle.dump(credentials,outp1,pickle.HIGHEST_PROTOCOL)
		
def readkey():
	global user
	print(user)
	try:
		with open(user+'datafilekey.pkl', 'rb') as inp:
			temp = pickle.load(inp)
			print("Data read")
			#print(credentials)
			return temp
	except:
		print("no cred data")
		return []

def sendOTP():
	global email
	global otp
	otp=genOtp()
	sendEmail(email,otp)
	
if __name__ == "__main__":
    context = ('server.crt', 'server.key')
    app.run(ssl_context=context, debug=False, host="0.0.0.0", port=5000)
