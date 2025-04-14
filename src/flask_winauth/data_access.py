import collections as _collections

import ntsecuritycon as _ntsecuritycon
import win32security as _win32security
import win32api as _win32api


TokenUserAccount = _collections.namedtuple("TokenUserAccount", "name domain account_type")


def get_token_user(token_handle: int) -> TokenUserAccount:
    """
    Get user information associated with a token, then release the token.
    """
    
    sid, attr = _win32security.GetTokenInformation(token_handle, _ntsecuritycon.TokenUser)
    _win32api.CloseHandle(token_handle)
    return TokenUserAccount(*_win32security.LookupAccountSid(None, sid))
