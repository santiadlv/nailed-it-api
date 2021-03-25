from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate(password: str, hash: str) -> bool:
    valid, new_hash = pwd_context.verify_and_update(password, hash)
    if valid:
        if new_hash:
            # Password rehashing and updating the database implementation pending
            pass 
        return True
    else:
        return False
