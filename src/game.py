from dataclasses import dataclass


@dataclass
class SteamGame:
    title: str
    description: str
    developer: str
    publisher: str
    rating: int
    review_count: int
    release_date: int
    features: list[str]
    tags: list[str]
    img: str
    min_sys_req: str
    rec_sys_req: str
