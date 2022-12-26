import inspect


class BaseEntity:
    id: str

    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            self.__setattr__(attr, value)

    def __str__(self) -> str:
        members = inspect.getmembers(self, lambda x: not (inspect.isroutine(x)))
        members = list(filter(lambda x: not str(x[0]).startswith("__"), members))

        res_str = ""
        for attr, value in members:
            res_str += f"{attr} -> {value}; "

        return res_str[:-1]

    def __repr__(self) -> str:
        return self.__str__()
