from django.db import models

import os
import json
from Cryptodome.Cipher import AES

MY_AES_KEY = str.encode(os.environ.get("MY_AES_KEY"))

class SecureToken(models.TextField):
    description = "Encrypted token value"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['blank'] = True
        kwargs['null'] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_length"]
        del kwargs["blank"]
        del kwargs["null"]
        return name, path, args, kwargs
    
    def encrypt_data(self, data):
        cipher = AES.new(MY_AES_KEY, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(str.encode(data))
        output = {
            'ciphertext': ciphertext.decode('ISO-8859-1'),
            'nonce': nonce.decode('ISO-8859-1'),
            'tag': tag.decode('ISO-8859-1')
            }

        test = str(ciphertext)

        output = json.dumps(output)
        return output

    def decrypt_data(self, data):
        data = json.loads(data)
        cipher = AES.new(MY_AES_KEY, AES.MODE_EAX, nonce=data['nonce'].encode('ISO-8859-1'))
        plaintext = cipher.decrypt(data['ciphertext'].encode('ISO-8859-1'))

        try:
            cipher.verify(data['tag'].encode('ISO-8859-1'))
            print("The message is authentic:", plaintext)
            return plaintext

        except ValueError:
            print("Key incorrect or message corrupted")
            return None
        
    def get_prep_value(self, value):
        #encrypt data with your own function
        return self.encrypt_data(value) 

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
    # decrypt data with your own function
        dc = self.decrypt_data(value)
        return dc