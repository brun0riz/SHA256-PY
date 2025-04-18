import os

class Config():
    BASE_DIR = os.getenv('BASE_DIR', 'C:\\Users\\Windows 11\\Documents\\Criptografia\\RSA')
    ARCHIVE_DIR = os.path.join(BASE_DIR, 'ARCHIVE')
    TEMPLATES_DIR = os.path.join(ARCHIVE_DIR, 'templates')
    