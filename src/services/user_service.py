import time
from datetime import datetime

import requests
from aiogram.types import User
from services.data_encrypt import DataEncrypt


class UserService:

    @staticmethod
    def register(user: User):
        auth_date = int(time.mktime(datetime.now().timetuple()))
        data_encrypt = DataEncrypt(authDate=auth_date, id=user.id, username=user.username, first_name=user.first_name,
                              last_name=user.last_name)

        data = {
            "telegramData": data_encrypt.data.replace("&", "\n"),
            "hash": data_encrypt.data_hash
        }

        requests.post("https://localhost:7128/api/identity/account/register", verify=False, json=data)

    @staticmethod
    def get_user_id(user_tg_id: str):
        response = requests.get(f"https://localhost:7128/api/users/userTgId/{user_tg_id}", verify=False)
        return None if response.status_code == 404 else response.json()
