from entitys.base_entity import BaseEntity


class MeetingInvite(BaseEntity):
    meetingId: str = None
    userId: str = None
    status: int = None
