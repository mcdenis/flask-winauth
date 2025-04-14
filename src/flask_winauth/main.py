import flask
import werkzeug.local

from . import data_access as _da


_AUTH_TOKEN_REQUEST_HEADER = "HTTP_X_IIS_WINDOWSAUTHTOKEN"
"""
The name of the HTTP header with the current user's token. The latter is created
and forwarded by IIS' HttpPlatformHandler when Windows Authentication is enabled
and `forwardWindowsAuthToken` is set to `true` in the HttpPlatformHandler
configuration.

See:
https://learn.microsoft.com/en-us/iis/extensions/httpplatformhandler/httpplatformhandler-configuration-reference#httpplatformhandler-configuration
"""


_EXTENSION_NAME = "winauth"
"""
Name of this extension, without the "flask_" prefix. Will be used as a prefix
for data in `flask.g`.
"""


_USER_KEY = "_" + _EXTENSION_NAME + "_user"
"""
Key referring to the logged-in user in `flask.g`.
"""


current_user: 'User' = werkzeug.local.LocalProxy(lambda: _get_user())
"""
The user currently logged-in.
"""


class User:
    def __init__(self, name: str, domain: str, account_type: int) -> None:
        self.name = name
        self.domain = domain
        self.account_type = account_type

    def __str__(self) -> str:
        return f"<User {self.domain}\{self.name}>"
        


def _get_user():
    if flask.has_request_context():
        if _USER_KEY not in flask.g:
            # First time the function is called for this request.
            h_token_str = flask.request.environ.get(_AUTH_TOKEN_REQUEST_HEADER)
            if h_token_str:
                # Found user handle in header; get associated info and store it
                # in a User object.
                h_token_int = int(h_token_str, 16)
                user_info = _da.get_token_user(h_token_int)
                user_obj = User(*user_info)
                setattr(flask.g, _USER_KEY, user_obj)
                # Log
                flask.current_app.logger.debug("Got user info from token : %s", user_obj)
            else:
                # No user info at our disposal.
                setattr(flask.g, _USER_KEY, None)
                flask.current_app.logger.debug("No user")
        return getattr(flask.g, _USER_KEY)
    return None