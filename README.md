# steam-scraping
Web scraping Steam game info and reviews using Selenium and BeautifulSoup4

The following Objects are outputed:

```python
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
```

```python
@dataclass
class SteamReview:
    text: str
    helpful: str
    recommendation: str
    rewards: int
    hrs_on_record: float
```
