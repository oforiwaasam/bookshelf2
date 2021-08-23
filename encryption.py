# encryption.py

# for keeping user passwords safe
#

from werkzeug.security import check_password_hash, generate_password_hash #install flask-bcrypt

# sha256 is a hashing algorithm
def encrypt_password(password):
    # Create hashed password
    password = generate_password_hash(password, method='sha256')
    return password
       

def check_password(self, password):
    # Check hashed password
    return check_password_hash(self.password, password) 