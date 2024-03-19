import dataclasses


@dataclasses.dataclass
class User:
    username: str
    password: str
    _id: str

    @classmethod
    def from_dict(cls, d):
        return cls(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
