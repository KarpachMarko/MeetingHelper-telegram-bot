from entitys.base_entity import BaseEntity


class Meeting(BaseEntity):
    title: str = None
    description: str = None
    startDate: str = None
    endDate: str = None
    budgetPerPerson: float = None
