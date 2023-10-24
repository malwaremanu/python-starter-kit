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
