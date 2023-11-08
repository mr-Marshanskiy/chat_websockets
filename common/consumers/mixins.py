class JWTConsumerMixin:
    def get_jwt_from_headers(self, lookup='authorization',):
        headers = self.get_headers()
        if lookup not in headers:
            return None
        token_name, token_key = headers[lookup].split()
        return token_key

    def get_jwt_from_params(self, lookup='token'):
        params = self.get_params()
        if lookup not in params:
            return None
        return params['token']
