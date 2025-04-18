from config import Config
from SIGNATURE.signMessage import sign_message, verify_signature

from ARCHIVE.encryptArchive import encrypt_file

def verify_authenticity(hash_original, hash_altered):
    print(f"Hash original: {hash_original}")
    print(f"Hash altered: {hash_altered}")

    if hash_original == hash_altered:
        print("The files are identical.")
    else:
        print("The file has been modified.")

def openfile(file_path):
    try:
        if file_path.endswith('.txt'):
            print("Opening file as text")
            with open(file_path, 'r', encoding='utf-8') as file:
                im =  file.read()
        else:
            with open(file_path, 'rb') as file:
                im =  file.read()
    except Exception as e:
        print("Error opening file:", e)
        return None
    
    return im

original_file = openfile(f'{Config.TEMPLATES_DIR}\\teste.txt')
altered_file = openfile(f'{Config.TEMPLATES_DIR}\\testeALT.txt')

hash_original = encrypt_file(original_file)
hash_altered = encrypt_file(altered_file)

verify_authenticity(hash_original, hash_altered)

# **************** SIGNATURE ********************

option = input("Do you want to sign a message? (y/n)")[0]

if  option.lower() == 'y':

    print(f"Hash SHA256: {hash_original}")

    hash_int = int(hash_original, 16) # convert hash to integer

    print(f"Hash int: {hash_int}")
    message_singed = sign_message(hash_int)

    print(f"Signature: {message_singed}")

    pd = int(input("Please, enter private exponent: "))   
    pn = int(input("Please, enter private modulus: "))

    print(f'Message signed: {message_singed}')

    original_message = hex(verify_signature(pd, pn, message_singed))
    print(f'Original message: {original_message}')
else:
    print("End of program.")