import cryptography
from cryptography import fernet as ft

key = ft.Fernet.generate_key()

a = ft.Fernet(key)


b = a.encrypt(b"testsetstsetts")
print(b)

print(a.decrypt(b))