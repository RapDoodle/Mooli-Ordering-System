import bcrypt

def verify_password(password, hashed_password):
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# hashed = hash_password('testpassword'.encode('utf-8'))
# print(hashed)
# print(verify_password('testpassword'.encode('utf-8'), hashed))
#
# new = b'$2b$12$tH7mKKfzgHu6XKxCpEcMr.5kg1l1P4jPYDPeOIoPoDjLy4DdOUlBq'
# print(verify_password('testpassword'.encode('utf-8'), new))
