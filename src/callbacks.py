from typing import Optional

from aiogram.utils.callback_data import CallbackData


class InviteMeetingCallback(CallbackData):
    KEY_MEETING_ID: str = "meeting_id"

    def __init__(self):
        super().__init__("invite_meeting_callback", self.KEY_MEETING_ID)

    def parse_meeting_id(self, callback_data: str) -> Optional[str]:
        return self.parse(callback_data)[self.KEY_MEETING_ID]


invite_meeting_callback = InviteMeetingCallback()


class InviteAnswerCallback(CallbackData):
    KEY_MEETING_ID: str = "meeting_id"
    KEY_ANSWER: str = "invite_answer"

    def __init__(self):
        super().__init__("answer_invite_callback", self.KEY_MEETING_ID, self.KEY_ANSWER)

    def new(self, meeting_id: str, invite_answer: str) -> str:
        return super().new(**{self.KEY_MEETING_ID: meeting_id, self.KEY_ANSWER: invite_answer})

    def parse_meeting_id(self, callback_data: str) -> Optional[str]:
        return self.parse(callback_data)[self.KEY_MEETING_ID]

    def parse_accepted(self, callback_data: str) -> Optional[bool]:
        return self.parse(callback_data)[self.KEY_ANSWER] == "acc"


invite_answer_callback = InviteAnswerCallback()
