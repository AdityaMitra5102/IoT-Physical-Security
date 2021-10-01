

"""
Example demo server to use a supported web browser to call the WebAuthn APIs
to register and use a credential.

See the file README.adoc in this directory for details.

Navigate to https://localhost:5000 in a supported web browser.
"""
from __future__ import print_function, absolute_import, unicode_literals

from fido2.webauthn import PublicKeyCredentialRpEntity
from fido2.client import ClientData
from fido2.server import U2FFido2Server
from fido2.ctap2 import AttestationObject, AuthenticatorData
from fido2.ctap1 import RegistrationData
from fido2.utils import sha256, websafe_encode
from fido2 import cbor
from flask import Flask, session, request, redirect, abort

import os


app = Flask(__name__, static_url_path="")
app.secret_key = os.urandom(32)  # Used for session.

rp = PublicKeyCredentialRpEntity("localhost", "Demo server")

server = U2FFido2Server("https://localhost:5000", rp)


credentials = []


@app.route("/")
def index():
    return redirect("/index-u2f.html")


@app.route("/api/register/begin", methods=["POST"])
def register_begin():
    registration_data, state = server.register_begin(
        {
            "id": b"user_id",
            "name": "a_user",
            "displayName": "A. User",
            "icon": "https://example.com/image.png",
        },
        credentials,
    )

    session["state"] = state
   
    return cbor.encode(registration_data)


@app.route("/api/register/complete", methods=["POST"])
def register_complete():
    data = cbor.decode(request.get_data())
    client_data = ClientData(data["clientDataJSON"])
    att_obj = AttestationObject(data["attestationObject"])
   

    auth_data = server.register_complete(session["state"], client_data, att_obj)

    credentials.append(auth_data.credential_data)
   
    return cbor.encode({"status": "OK"})


@app.route("/api/authenticate/begin", methods=["POST"])
def authenticate_begin():
    if not credentials:
        abort(404)

    auth_data, state = server.authenticate_begin(credentials)
    session["state"] = state
    return cbor.encode(auth_data)


@app.route("/api/authenticate/complete", methods=["POST"])
def authenticate_complete():
    if not credentials:
        abort(404)

    data = cbor.decode(request.get_data())
    credential_id = data["credentialId"]
    client_data = ClientData(data["clientDataJSON"])
    auth_data = AuthenticatorData(data["authenticatorData"])
    signature = data["signature"]
   

    server.authenticate_complete(
        session.pop("state"),
        credentials,
        credential_id,
        client_data,
        auth_data,
        signature,
    )
  
    return cbor.encode({"status": "OK"})





@app.route("/api/u2f/begin", methods=["POST"])
def u2f_begin():
    registration_data, state = server.register_begin(
        {
            "id": b"user_id",
            "name": "a_user",
            "displayName": "A. User",
            "icon": "https://example.com/image.png",
        },
        credentials,
    )

    session["state"] = state
  
    return cbor.encode(websafe_encode(registration_data["publicKey"]["challenge"]))


@app.route("/api/u2f/complete", methods=["POST"])
def u2f_complete():
    data = cbor.decode(request.get_data())
    client_data = ClientData.from_b64(data["clientData"])
    reg_data = RegistrationData.from_b64(data["registrationData"])
  
    att_obj = AttestationObject.from_ctap1(sha256(b"https://localhost:5000"), reg_data)
  

    auth_data = att_obj.auth_data

    credentials.append(auth_data.credential_data)
  
    return cbor.encode({"status": "OK"})


if __name__ == "__main__":
    
    app.run(ssl_context="adhoc", debug=False)
