import os
import base64
from cryptography.fernet import Fernet
from typing import Optional

class EncryptionService:
    def __init__(self, encryption_key: Optional[str] = None):
        if encryption_key is None:
            encryption_key = os.environ.get('ENCRYPTION_KEY')
            
        if encryption_key is None:
            key_file = '.encryption_key'
            if os.path.exists(key_file):
                try:
                    with open(key_file, 'r') as f:
                        encryption_key = f.read().strip()
                    os.environ['ENCRYPTION_KEY'] = encryption_key
                    print(f"✓ Loaded encryption key from {key_file}")
                except Exception as e:
                    print(f"⚠️  ERROR: Failed to load encryption key from {key_file}: {e}")
                    raise RuntimeError("Encryption key file corrupted")
            else:
                encryption_key = Fernet.generate_key().decode()
                os.environ['ENCRYPTION_KEY'] = encryption_key
                try:
                    with open(key_file, 'w') as f:
                        f.write(encryption_key)
                    os.chmod(key_file, 0o600)
                    print(f"⚠️  IMPORTANT: Generated new encryption key and saved to {key_file}")
                    print(f"   Keep this file safe! Losing it means encrypted data cannot be recovered.")
                    print(f"   For production: Set ENCRYPTION_KEY environment variable instead.")
                    print(f"   ENCRYPTION_KEY={encryption_key}")
                except Exception as e:
                    print(f"⚠️  WARNING: Could not save key to file: {e}")
                    print(f"   Set this in your environment: ENCRYPTION_KEY={encryption_key}")
        
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
