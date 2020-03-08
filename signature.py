# Signature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import exceptions as cryptographyExceptions
from cryptography.hazmat.primitives import serialization

def generate_keys():
    private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
    )

    serialized_public_key = private_key.public_key().public_bytes(
       encoding=serialization.Encoding.PEM,
       format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key, serialized_public_key

def sign(message, private_key):
    message = bytes(str(message), 'utf-8')
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

def verify(message, signed_message, public_key):
    message = bytes(str(message), 'utf-8')

    public_key = serialization.load_pem_public_key(
    public_key,
    backend=default_backend()
)

    try:
            public_key.verify(
                signed_message,
                message,
                padding.PSS(
                            mgf=padding.MGF1(hashes.SHA256()),
                            salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
    except cryptographyExceptions.InvalidSignature:
            return False
    except:
            print("Error executing public_key.verify")
            return False

if __name__ == '__main__':
    print("signature.py tests start here")

    # sign_process_is_valid:
    private_key, public_key = generate_keys();
    message = 'ramin message';
    signed_message = sign(message, private_key);
    result = verify(message, signed_message, public_key)
    if not result: print("Error: we shouldn't give any error.")

    # sign_process_is_valid:
    private_key, public_key = generate_keys();
    message = 'ramin message';
    signed_message = sign(message, private_key);
    result = verify('message', signed_message, public_key)
    if result: print("Error: we shouldn give an error hence we change the original message.")

    print('If you do not see any printed message on your console, that means every tests passed successfully.')
