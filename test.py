import cryptography
from cryptography import fernet as ft
from cryptography.hazmat.primitives.asymmetric import rsa as rsa


key = ft.Fernet.generate_key()

a = ft.Fernet(key)



b = a.encrypt(b"testsetstsetts")
print(b)

print(a.decrypt(b))
#rsa.RSABackend()
#rsa.
#backend = rsa.RSABackend()
#
#a = rsa.generate_private_key(16, 64, backend)
#print(a)

public = rsa.RSAPublicKey()
#v = ft.Cipher(cryptography.hazmat.primitives.ciphers.algorithms.AES(b"stestste984854785757575757777777") ,cryptography.hazmat.primitives.ciphers.base.AEADCipherContext(),  cryptography.hazmat.backends.default_backend())
#
#
#v_enc = v.encryptor()
#v_enc.authenticate_additional_data("test")
#
#v_enc.finalize()
#print(v_enc)