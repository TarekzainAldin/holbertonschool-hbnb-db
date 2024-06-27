from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def generate_password_hash(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password_hash(password_hash: str, password: str) -> bool:
    return bcrypt.check_password_hash(password_hash, password)
