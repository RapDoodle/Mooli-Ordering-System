import bcrypt

def verify_password(password, hashed_password):
    passwprd = str(password).strip()
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    return False

def hash_password(password):
    passwprd = str(password).strip()
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# hashed = bcrypt.hashpw('testpass'.encode('utf-8'), bcrypt.gensalt())
# print(len(hashed))
# print(verify_password('Testpassword123', b'$2b$12$k5AdTMgoaNd889RKRWIlQufZ6BUSnbtfMzD/b3PFEOKku70KDVPUS'))
#
# new = b'$2b$12$tH7mKKfzgHu6XKxCpEcMr.5kg1l1P4jPYDPeOIoPoDjLy4DdOUlBq'
# print(verify_password('testpassword'.encode('utf-8'), new))
# print(len(hashed))
