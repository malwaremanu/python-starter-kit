# token_validation.py
from fastapi import HTTPException, Depends, Header
from typing import Optional
from config import get_kinde_client, config
import jwt
from requests import get

async def validate_token(authorization: str = Header(...)):  # '...' makes the header field required
    scheme, _, jwt_token = authorization.partition(' ')
    if scheme.lower() != 'bearer':
        raise HTTPException(status_code=401, detail='Invalid scheme type')
    if not jwt_token:
        raise HTTPException(status_code=401, detail='Token not found')

    kinde_client = get_kinde_client()
    jwks_url = config['KINDE_ISSUER_URL'] + "/.well-known/jwks"
    jwks_response = get(jwks_url)
    jwks_data = jwks_response.json()
    jwks_keys = jwks_data['keys']
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks_keys[0])

    try:
        # Validate the JWT using the public key
        decoded_token = jwt.decode(jwt_token, public_key, algorithms=["RS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return { "error" : "Token has expired."}
    except jwt.InvalidTokenError as e:
        return { "error" : str(e)}

