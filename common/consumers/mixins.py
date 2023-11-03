class JWTConsumerMixin:
    def get_jwt_from_headers(self, lookup='authorization',):
        headers = self.get_headers()
        if lookup not in headers:
            return None
        token_name, token_key = headers[lookup].split()
        return token_key
