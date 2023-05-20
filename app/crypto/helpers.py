from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends import default_backend
import binascii

def get_keys_from_cert(file_path):
    with open(file_path, 'rb') as key_file:
        private_key = load_pem_private_key(key_file.read(), None, default_backend())
        private_numbers = private_key.private_numbers()
        public_pt = private_key.public_key().public_numbers()
        
        private_key_int = private_numbers.private_value
        
        return (private_key_int, (public_pt.x, public_pt.y))
