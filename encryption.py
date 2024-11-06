from cryptography.fernet import Fernet

key = Fernet.generate_key()
with open("encrypt.key", "wb") as encryptkey:
    encryptkey.write(key)
