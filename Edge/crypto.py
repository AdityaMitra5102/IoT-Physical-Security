from cryptography.fernet import Fernet

key0='5ixShgImEPABctRel37XWCw1YC70G4ZconyzJxRrgek='
key1='Cgv9KLrsX4RPJI9S8wQ38CYHnct_KSa1RmeXGImoZpA='
key2='nn995tvh5dDSUavtQgc6NC9ZgW-wHF6XqZz6nIIT5ho='
key3='9xPJaiSHNl75yKUHq_KW9_OSASXXgSFhrECmFpBG7Rg='
key4='IJFYkHIppGZ-1zTzzM8HANRupPl7Zvdq6XvTFKEq8C4='
key5='Kdf9mjtCRJfXAI2Hl0pBfVscQ01_mQ7ZeT-hYJj6qnI='


def encrypt(plaintext, key):
	k=key.encode()
	fernet=Fernet(k)
	encMessage=fernet.encrypt(plaintext.encode())
	cipher=encMessage.decode()
	return cipher
	
def decrypt(cipher, key):
	k=key.encode()
	fernet=Fernet(k)
	decMessage=fernet.decrypt(cipher.encode())
	plaintext=decMessage.decode()
	return plaintext
	
