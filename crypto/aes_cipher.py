from Crypto.Cipher import AES
import base64
import hashlib

def pad(data):
    return data + (16 - len(data) % 16) * chr(16 - len(data) % 16)

def unpad(data):
    return data[:-ord(data[-1])]

def encrypt_aes(data, key):
    key = hashlib.sha256(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(data).encode())
    return base64.b64encode(ct_bytes).decode()

def decrypt_aes(enc_data, key):
    key = hashlib.sha256(key.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    pt = cipher.decrypt(base64.b64decode(enc_data))
    return unpad(pt.decode())
