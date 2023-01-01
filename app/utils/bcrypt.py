from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_pass(password: str) -> str:
    return password_context.hash(password)

def verify_hash_pass(password: str, hash: str) -> bool:
    return password_context.verify(password, hash)