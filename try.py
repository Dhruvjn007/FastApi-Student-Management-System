from auth_utils import hash_password, verify_password

password = "mypassword1233"

hashed = hash_password(password)

print(verify_password(password,hashed))
print(verify_password("wrong_pass",hashed))