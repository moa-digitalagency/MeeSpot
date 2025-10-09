#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

import os
import base64
from cryptography.fernet import Fernet
from typing import Optional

class EncryptionService:
    def __init__(self, encryption_key: Optional[str] = None):
        if encryption_key is None:
            encryption_key = os.environ.get('ENCRYPTION_KEY')
            
        if encryption_key is None:
            raise RuntimeError(
                "ENCRYPTION_KEY environment variable is required but not set.\n"
                "Please set ENCRYPTION_KEY in your environment variables.\n"
                "You can generate a key using: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
            )
        
        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode()
        
        self.fernet = Fernet(encryption_key)
    
    def encrypt(self, plaintext: Optional[str]) -> Optional[str]:
        if plaintext is None or plaintext == '':
            return None
        
        try:
            encrypted_bytes = self.fernet.encrypt(plaintext.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_bytes).decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {e}")
            return plaintext
    
    def decrypt(self, ciphertext: Optional[str]) -> Optional[str]:
        if ciphertext is None or ciphertext == '':
            return None
        
        try:
            encrypted_bytes = base64.urlsafe_b64decode(ciphertext.encode('utf-8'))
            decrypted_bytes = self.fernet.decrypt(encrypted_bytes)
            return decrypted_bytes.decode('utf-8')
        except Exception as e:
            print(f"Decryption error: {e}")
            return ciphertext

encryption_service = EncryptionService()

def encrypt_value(value: Optional[str]) -> Optional[str]:
    return encryption_service.encrypt(value)

def decrypt_value(value: Optional[str]) -> Optional[str]:
    return encryption_service.decrypt(value)
