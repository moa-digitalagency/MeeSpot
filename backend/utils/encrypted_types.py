#
# MatchSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from sqlalchemy.types import TypeDecorator, String
from backend.utils.encryption import encrypt_value, decrypt_value

class EncryptedString(TypeDecorator):
    impl = String
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return encrypt_value(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is not None:
            return decrypt_value(value)
        return value

class EncryptedText(TypeDecorator):
    impl = String
    cache_ok = True
    
    def process_bind_param(self, value, dialect):
        if value is not None:
            return encrypt_value(value)
        return value
    
    def process_result_value(self, value, dialect):
        if value is not None:
            return decrypt_value(value)
        return value
