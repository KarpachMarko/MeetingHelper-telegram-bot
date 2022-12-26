from typing import List

import requests

from entitys.meeting import Meeting
from services.base_service import BaseService


class MeetingService(BaseService):

    def get_all(self) -> List[Meeting]:
        response = requests.get("https://localhost:7128/api/meetings", verify=False, headers=self.get_headers())
        json_list = response.json()
        meetings: List[Meeting] = []
        for json in json_list:
            meetings.append(Meeting(**json))

        return meetings

    def get(self, meeting_id: str) -> Meeting:
        response = requests.get(f"https://localhost:7128/api/meetings/{meeting_id}", verify=False,
                                headers=self.get_headers())
        json = response.json()
        return Meeting(**json)
