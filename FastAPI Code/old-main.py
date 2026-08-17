from datetime import date

from typing import Union
from fastapi import FastAPI, Request

app = FastAPI()

# ---------------- Config Started
# Kinde Configuration
from kinde_sdk.kinde_api_client import GrantType

SITE_HOST = "localhost"
SITE_PORT = "5000"
SITE_URL = f"http://{SITE_HOST}:{SITE_PORT}"
LOGOUT_REDIRECT_URL = f"http://{SITE_HOST}:{SITE_PORT}/api/auth/logout"
KINDE_CALLBACK_URL = f"http://{SITE_HOST}:{SITE_PORT}/api/auth/kinde_callback"
CLIENT_ID = "271ff28f32b740b5ae2d6f9fb1ab084e"
CLIENT_SECRET = "UYMFCOqThZZILboPkWlQwORmv1JaXxoZ4nXSTFirer84jTuYqsavy"
KINDE_ISSUER_URL = "https://nsfdc-dev.eu.kinde.com"
GRANT_TYPE = GrantType.AUTHORIZATION_CODE_WITH_PKCE
CODE_VERIFIER = "joasd923nsad09823noaguesr9u3qtewrnaio90eutgersgdsfg" # A suitably long string > 43 chars
TEMPLATES_AUTO_RELOAD = True
SESSION_TYPE = "filesystem"
SESSION_PERMANENT = False
SECRET_KEY = "joasd923nsad09823noaguesr9u3qtewrnaio90eutgersgdsfgs" # Secret used for session management


import jwt
from requests import get  # You may need to install the requests library

# The JWT token you want to validate
jwt_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk2OmM4OjkzOjU1OjNlOmRiOmNjOjg5OmNjOjk4OjBhOmQxOmIzOjlmOmRhOjUyIiwidHlwIjoiSldUIn0.eyJhdWQiOltdLCJhenAiOiIyNzFmZjI4ZjMyYjc0MGI1YWUyZDZmOWZiMWFiMDg0ZSIsImV4cCI6MTY5ODIyMzQ3MCwiaWF0IjoxNjk4MTM3MDcwLCJpc3MiOiJodHRwczovL25zZmRjLWRldi5ldS5raW5kZS5jb20iLCJqdGkiOiJjY2E0MmVmZi02ZDM1LTRmNWQtYWEyMC0zM2ZkOWI2ZTI3NWUiLCJvcmdfY29kZSI6Im9yZ19kNWQ3NGMzNWM5Y2MiLCJwZXJtaXNzaW9ucyI6WyJzYW1wbGVfcGVybWlzc2lvbiJdLCJzY3AiOlsib3BlbmlkIiwicHJvZmlsZSIsImVtYWlsIiwib2ZmbGluZSJdLCJzdWIiOiJrcF9hYTFmMTQyNmI5OTQ0N2EzODMwNjkxZmVkZjE4ODUzOCJ9.jTdgtrox6fAzOIt-4bu4UTGkMPjkQWRwW_B-1jtCud8r2ExPYZKEP7_FpjPaUnNfy2PzYX-RMxDTmtJ_K3tyiw3iVNd21WmZJNlQIpAFSQ4JwgTu3lcuvWWa5z-c5vdvJCCAahiZnHFpembJqKiCwfsRHZn1pMujgNBSJwzBTExfJMfNAxY45CTko1S3YPjuwIFNJDJFLiQ26H3Y93i8llpm6GWuF9AAF2CukLipunuDFGsN7l3uX4RguvZciyefe2bRAFkzTmuZY6gYeUZKOjvLGBEux_ysExKRKTrwQqaDomHso6FWtbXwzTKt2ktonlPiOONPiKEbsyP2uNw6Yg"
jwks_url = KINDE_ISSUER_URL + "/.well-known/jwks"
jwks_response = get(jwks_url)
jwks_data = jwks_response.json()
jwks_keys = jwks_data['keys']
public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks_keys[0])

# Kinde implementation
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient

configuration = Configuration(KINDE_ISSUER_URL)

kinde_api_client_params = {
    "configuration": configuration,
    "domain": KINDE_ISSUER_URL,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "grant_type": GRANT_TYPE,
    "callback_url": KINDE_CALLBACK_URL,
}
if GRANT_TYPE == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
    kinde_api_client_params["code_verifier"] = CODE_VERIFIER

kinde_client = KindeApiClient(**kinde_api_client_params)
user_clients = {}

# ------- Configuration Ended

def get_authorized_data(kinde_client):
    user = kinde_client.get_user_details()
    return {
        "id": user.get("id"),
        "user_given_name": user.get("given_name"),
        "user_family_name": user.get("family_name"),
        "user_email": user.get("email"),
        "user_picture": user.get("picture"),
    }

@app.get("/api/auth/login")
def login_url():
    return {
        "url" : str(kinde_client.get_login_url())
    }

@app.get("/api/auth/kinde_callback")
def auth_url(request: Request):    
    kinde_client.fetch_token(authorization_response=str(request.url))
    data = {"current_year": date.today().year}
    data.update(get_authorized_data(kinde_client))

    token = kinde_client.configuration.access_token
    permissions = kinde_client.get_permissions()            
    return {
        "user_clients" : data,
        "token" : token,
        "permissions" : permissions
    }


@app.get("/api/auth/validate")
def validate_token():
    try:
        # Validate the JWT using the public key
        decoded_token = jwt.decode(jwt_token, public_key, algorithms=["RS256"])
        print("Token is valid")
        return {
            "success" : decoded_token
        }
    except jwt.ExpiredSignatureError:
        return { "error" : "Token has expired."}
    except jwt.InvalidTokenError as e:
        return { "error" : "Token has expired." + str(e)}