# steam-scraping
Web scraping Steam game info and reviews using Selenium and BeautifulSoup4

Proof of legality of scarping and crawling:

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

The `SteamGame` data is fetched using the following input:
```
https://store.steampowered.com/app/{game_id}/
```

https://store.steampowered.com/robots.txt:
```
Host: store.steampowered.com
User-Agent: *
Disallow: /share/
Disallow: /news/externalpost/
Disallow: /account/emailoptout/?*token=
Disallow: /login/?*guestpasskey=
Disallow: /join/?*redir=
Disallow: /account/ackgift/
Disallow: /email/
Disallow: /widget/
```

The `SteamReview` data is fetched using the following endpoint:
```
https://steamcommunity.com/app/{game_id}/reviews/?p=1&browsefilter=toprated
```

https://steamcommunity.com/robots.txt:
```
User-agent: *
Disallow: /actions/
Disallow: /linkfilter/
Disallow: /tradeoffer/
Disallow: /trade/
Disallow: /email/
Host: steamcommunity.com
```