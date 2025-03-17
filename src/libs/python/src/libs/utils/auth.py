from jwt import encode, decode, InvalidTokenError
import os

SECRET_KEY = 'token'

def extract_token_from_header(auth_header):
    """
    Extracts the JWT token from the authorization header.
    
    :param auth_header: Authorization header containing the Bearer token
    :return: JWT token if present, None otherwise
    """
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.split(" ")[1]
    return None

def validate_token(token):
    """
    Validates a JWT token.
    
    :param token: JWT token to be validated
    :return: Decoded token if valid, None otherwise
    """
    try:
        decoded_token = decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except InvalidTokenError:
        return None

def generate_token():
    """
    Generates a JWT token from the word 'ChallengeDAtaAPI2025'.
    
    :return: JWT token
    """
    payload = {
        'data': 'ChallengeDAtaAPI2025'
    }
    token = encode(payload, SECRET_KEY, algorithm="HS256")
    return token