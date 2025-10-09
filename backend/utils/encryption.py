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
from typing import Optional, Union

class EncryptionService:
    def __init__(self, encryption_key: Optional[str] = None):
        key: Union[str, bytes, None] = encryption_key
        if key is None:
            key = os.environ.get('ENCRYPTION_KEY')
            
        if key is None:
            key = Fernet.generate_key()
            os.environ['ENCRYPTION_KEY'] = key.decode()
            print(f"⚠️  ENCRYPTION_KEY auto-generated. Add this to your environment variables for persistence:")
            print(f"ENCRYPTION_KEY={key.decode()}")
        
        if isinstance(key, str):
            key = key.encode()
        
        self.fernet = Fernet(key)
    
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
