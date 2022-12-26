from typing import List

import requests

from entitys.meetingInvite import MeetingInvite
from services.base_service import BaseService


class MeetingInviteService(BaseService):

    def send_invite(self, meeting_id: str, user_id: str) -> bool:
        data = {
            "meetingId": meeting_id,
            "userId": user_id
        }
        response = requests.post("https://localhost:7128/api/meetingInvites/unanswered", verify=False, headers=self.get_headers(), json=data)
        return 200 <= response.status_code < 300

    def get_unanswered(self) -> List[MeetingInvite]:
        response = requests.get("https://localhost:7128/api/meetingInvites/unanswered", verify=False, headers=self.get_headers())
        json_list = response.json()
        invites: List[MeetingInvite] = []
        for json in json_list:
            invites.append(MeetingInvite(**json))

        return invites

    def accept_invite(self, meeting_id: str):
        requests.get(f"https://localhost:7128/api/meetingInvites/meeting/{meeting_id}/accept", verify=False, headers=self.get_headers())

    def reject_invite(self, meeting_id: str):
        requests.get(f"https://localhost:7128/api/meetingInvites/meeting/{meeting_id}/reject", verify=False, headers=self.get_headers())
