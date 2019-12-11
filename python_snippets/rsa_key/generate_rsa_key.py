import jwt

from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend, default_backend

key = rsa.generate_private_key(
    backend=crypto_default_backend(),
    public_exponent=65537,
    key_size=2048
)

private_key = key.private_bytes(
    crypto_serialization.Encoding.PEM,
    crypto_serialization.PrivateFormat.TraditionalOpenSSL,
    crypto_serialization.NoEncryption())

public_key = key.public_key().public_bytes(
    crypto_serialization.Encoding.OpenSSH,
    crypto_serialization.PublicFormat.OpenSSH
)

with open("private.pem", "w") as f:
    f.write(private_key.decode('utf-8'))

with open("public.pem", "w") as f:
    f.write(public_key.decode('utf-8'))

# with open('private.pem', mode='rb') as private:
#     private_key = private.read()
#
# with open('public.pem', mode='rb') as public:
#     public_key = public.read()

encoded_jwt = jwt.encode({'some': 'payload'}, private_key, algorithm='RS256')
print(encoded_jwt)
print(jwt.decode(encoded_jwt, public_key, algorithms=['RS256']))



