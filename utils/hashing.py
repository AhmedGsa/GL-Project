from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password):
        return pwd_context.hash(password)
    
    def compare(hash, password):
        return pwd_context.verify(password, hash)