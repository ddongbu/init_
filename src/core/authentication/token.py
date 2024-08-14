
from datetime import datetime, timedelta

import jwt


class VdreamToken:
    def __init__(self, **kwargs):
        self.secret_key = kwargs.get("JWT_SECRET_KEY")
        self.algorithm = kwargs.get("JWT_ALGORITHM")
        self.access_token_expire_minutes = int(kwargs.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.refresh_token_expire_days = int(kwargs.get("REFRESH_TOKEN_EXPIRE_DAYS"))

    def encode(self, payload):
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode(self, token):
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

    def create_access_token(self, data):
        expire = datetime.now() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        encoded_jwt = self.encode(to_encode)
        return encoded_jwt

    def create_refresh_token(self, data: dict, ip: str):
        expire = datetime.now() + timedelta(days=self.refresh_token_expire_days)
        to_encode = data.copy()
        to_encode.update({"exp": expire, "ip": ip})
        encoded_jwt = self.encode(to_encode)
        return encoded_jwt

    def generate_token(self, sub: str, ip: str):
        access_token = self.create_access_token(data={"sub": sub})
        refresh_token = self.create_refresh_token(data={"sub": sub}, ip=ip)
        return access_token, refresh_token
