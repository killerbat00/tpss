from Crypto.Cipher import AES
import base64
from functools import wraps
from skateapp import app
from flask import flash, g, url_for, redirect, request, abort

KEY=app.config['SECRET_KEY']

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

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(u'You need to be signed in to view this page.')
            return redirect(url_for('general.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function
