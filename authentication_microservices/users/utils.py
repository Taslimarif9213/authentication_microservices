import bcrypt
import re
from core.constants.message import PASSWORD_UPDATE
from exception_handler.generic_exception import BadRequest


# Function to check if a mobile number is valid
def is_valid_mobile_number(mobile_no):
    if len(mobile_no) == 10:  # Check if the number has exactly 10 digits
        return True
    else:
        return False


# Function to check if an email address is valid
def is_valid_email(email):
    # Define a regular expression pattern for a valid email address
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # Use the re.match function to check if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False


# Function to hash a password using bcrypt
def bcrypt_hash_password(password):
    try:
        # Hash the password using bcrypt with a specified number of rounds
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode()
        return hashed_password
    except ValueError:
        # If there's an error during hashing, raise a BadRequest exception with a specific message
        raise BadRequest(detail=PASSWORD_UPDATE)


def validated_hashed_password(password, hashed_password):
    try:
        return True if bcrypt.checkpw(password.encode("utf8"), hashed_password.encode("utf8")) else False
    except ValueError:
        raise BadRequest(detail=PASSWORD_UPDATE)
