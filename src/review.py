from dataclasses import asdict, dataclass


@dataclass
class SteamReview:
    text: str
    helpful: str
    recommendation: str
    rewards: int
    hrs_on_record: float

    def to_dict(self):
        return asdict(self)
