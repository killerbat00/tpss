from Crypto.Cipher import AES
import base64
#from skateapp import app

#KEY=app.config['SECRET_KEY']
KEY='skateappskateapp'

def encrypt(val):
    enc_secret = AES.new(KEY)
    tag_string = (str(val) +
                 (AES.block_size -
                len(str(val)) % AES.block_size) * "\0")
    cipher_text = base64.b64encode(enc_secret.encrypt(tag_string))
    return cipher_text

def decrypt(val):
    dec_secret = AES.new(KEY)
    raw_decrypted = dec_secret.decrypt(base64.b64decode(val))
    clear_val = raw_decrypted.rstrip("\0")
    return clear_val
