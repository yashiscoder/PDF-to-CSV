from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()
ip_pwd="hello"
password = "hello"
hashed_pwd = ph.hash(password)

print(hashed_pwd)

try:
    ph.verify(hashed_pwd,ip_pwd)
    print("Correct")
except VerifyMismatchError:
    print("invalid")