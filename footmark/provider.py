
"""
This class encapsulates the provider-specific header differences.
"""

class Provider(object):

    def __init__(self, name, access_key=None, secret_key=None, security_token=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.security_token = security_token
        
    def get_access_key(self):
        # if self._credentials_need_refresh():
        #     self._populate_keys_from_metadata_server()
        return self._access_key

    def set_access_key(self, value):
        self._access_key = value

    access_key = property(get_access_key, set_access_key)

    def get_secret_key(self):
        # if self._credentials_need_refresh():
        #     self._populate_keys_from_metadata_server()
        return self._secret_key

    def set_secret_key(self, value):
        self._secret_key = value

    secret_key = property(get_secret_key, set_secret_key)

    def get_security_token(self):
        if self._credentials_need_refresh():
            self._populate_keys_from_metadata_server()
        return self._security_token

    def set_security_token(self, value):
        self._security_token = value

    security_token = property(get_security_token, set_security_token)

# Static utility method for getting default Provider.
def get_default():
    return Provider('acs')
