import hashlib
import hmac
import os
from typing import List


class DataEncrypt:

    _header_data: str
    _header_hash: str

    def __init__(self, **kwargs):

        pairs: List[str] = []

        for key, value in kwargs.items():
            pairs.append(f"{key}={value}")

        pairs.sort()
        header_data = "&".join(pairs)

        bot_token = os.environ.get("mh_bot_token") or ""
        secret_key = hmac.new(b"WebAppData", msg=bot_token.encode("utf-8"), digestmod=hashlib.sha256)

        header_hash = hmac.new(secret_key.digest(), msg=header_data.replace("&", "\n").encode("utf-8"), digestmod=hashlib.sha256).hexdigest().upper()

        self._header_data = header_data
        self._header_hash = header_hash

    @property
    def data(self) -> str:
        return self._header_data

    @property
    def data_hash(self) -> str:
        return self._header_hash
