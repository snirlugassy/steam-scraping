import json

from src.scrape import scrape_game_reviews_page
from src.scrape import scrape_game_store_page

games = [
    594650,
    261550,
    389730,
    774171,
    221680,
    1644960,
    453480,
    594650,
    552520,
    1423600,
    333600,
    1597580,
    1091500,
    1222700,
    108600,
    766570,
    1222670,
    1097150,
    773370,
    252490,
    381210,
    105600
]

data = []
for game in games:
    steam_game = scrape_game_store_page(game)
    print(steam_game)

    steam_reviews = scrape_game_reviews_page(game, review_limit=100)
    print(steam_reviews)

    data.append({
        'game': steam_game.to_dict(),
        'reviews': [r.to_dict() for r in steam_reviews]
    })

with open('data.json', 'w') as f:
    json.dump(data, f)