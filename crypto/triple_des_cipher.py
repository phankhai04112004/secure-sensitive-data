from Crypto.Cipher import DES3
import base64
import hashlib

# Thêm padding (PKCS5)
def pad(data):
    pad_len = 8 - len(data) % 8
    return data + chr(pad_len) * pad_len

# Bỏ padding
def unpad(data):
    return data[:-ord(data[-1])]

def encrypt_3des(data, key):
    key = hashlib.sha256(key.encode()).digest()[:24]
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded_data = pad(data).encode()
    ct_bytes = cipher.encrypt(padded_data)
    return base64.b64encode(ct_bytes).decode()

def decrypt_3des(enc_data, key):
    key = hashlib.sha256(key.encode()).digest()[:24]
    cipher = DES3.new(key, DES3.MODE_ECB)
    pt = cipher.decrypt(base64.b64decode(enc_data))
    return unpad(pt.decode())
