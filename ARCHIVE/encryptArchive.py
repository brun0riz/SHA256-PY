from BASE64.base import encrypt_base64
from SHA256.SHA256 import generate_hash

def encrypt_file(file):

    sha_image =  generate_hash(file)

    return sha_image