import time
from datetime import datetime
from typing import Dict

from services.data_encrypt import DataEncrypt


class BaseService:
    _user_id: str
    _username: str

    def __init__(self, user_id: str, username: str):
        self._user_id = user_id
        self._username = username

    def get_headers(self) -> Dict[str, str]:
        auth_date = int(time.mktime(datetime.now().timetuple()))
        encrypted_data = DataEncrypt(authDate=auth_date, id=self._user_id, username=self._username)
        return {
            "AuthorizationData": encrypted_data.data,
            "AuthorizationHash": encrypted_data.data_hash
        }
