# config.py
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient
import jwt
from requests import get

# Configuration
config = {
    "SITE_URL": "http://localhost:5000",
    "CLIENT_ID": "271ff28f32b740b5ae2d6f9fb1ab084e",
    "CLIENT_SECRET": "UYMFCOqThZZILboPkWlQwORmv1JaXxoZ4nXSTFirer84jTuYqsavy",
    "KINDE_ISSUER_URL": "https://nsfdc-dev.eu.kinde.com",
    "GRANT_TYPE": GrantType.AUTHORIZATION_CODE_WITH_PKCE,
    "CODE_VERIFIER": "joasd923nsad09823noaguesr9u3qtewrnaio90eutgersgdsfg",  # A suitably long string > 43 chars
}

def get_kinde_client():
    configuration = Configuration(config["KINDE_ISSUER_URL"])
    kinde_api_client_params = {
        "configuration": configuration,
        "domain": config["KINDE_ISSUER_URL"],
        "client_id": config["CLIENT_ID"],
        "client_secret": config["CLIENT_SECRET"],
        "grant_type": config["GRANT_TYPE"],
        "callback_url": f"{config['SITE_URL']}/api/auth/kinde_callback",
    }
    if config["GRANT_TYPE"] == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
        kinde_api_client_params["code_verifier"] = config["CODE_VERIFIER"]
    return KindeApiClient(**kinde_api_client_params)
