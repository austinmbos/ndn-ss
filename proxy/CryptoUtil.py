
"""
 Using python 3.7
 ==========================
 ==     install          ==
 ==========================
 $ pip install cryptography

 Makes the assumption it will be working with data
 as strings. 
"""
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.backends import default_backend


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization



from cryptography.hazmat.primitives import hashes

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes




def create_sym_key():
    return os.urandom(32)

def create_sym_key_and_iv():
    return os.urandom(32), os.urandom(16)


def sym_encrypt(key,data):
    iv = b'111111111111'
    encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv), 
            backend=default_backend()
            ).encryptor()
    #encryptor.authenticate_additional_data(bytes("","utf-8"))

    ct = encryptor.update(bytes(data,"utf-8")) + encryptor.finalize()
    return (iv, ct, encryptor.tag)

def sym_decrypt(key,iv,ct,tag):
    """ pass in the key, iv, ciphertext, and cipher tag
        to do the decryption
    """
    decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv,tag),
            backend=default_backend()
            ).decryptor()

    #decryptor.authenticate_additional_data(bytes("","utf-8"))

    return decryptor.update(ct) + decryptor.finalize()


def gen_rsa_priv_key():
    """ Generate a private key
        default key size is 4096
        default exponent is 65537

        return: you bet, a private key
    """
    priv_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=4096,
            backend=default_backend()
            )

    return priv_key


def rsa_enc(pub_key,data):
    ct = pub_key.encrypt(bytes(data,'utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    return ct

def rsa_dec(priv_key,ct):
    pt = priv_key.decrypt(ct,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
                )
            )
    return pt

def gen_priv_key():
    priv_key = Ed25519PrivateKey.generate()
    return priv_key


def get_pub_key(priv_key):
    return priv_key.public_key()


def get_priv_bytes(priv_key):
    bytes = priv_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
            )
    return bytes

def get_pub_bytes(pub_key):
    bytes = pub_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
            )
    return bytes

def load_priv_key(priv_key_bytes):
    return ed25519.Ed25519PrivateKey.from_private_bytes(priv_key_bytes)

def load_pub_key(pub_key_bytes):
    return ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)



if __name__ == "__main__":
    print("CryptoUtil")

    priv_key = gen_rsa_priv_key()
    pub_key = priv_key.public_key()

    data = "test"
    ct = rsa_enc(pub_key,data)
    pt = rsa_dec(priv_key,ct)
    print(pt)
   


    


