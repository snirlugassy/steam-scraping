import json

from src.scrape import scrape_game_reviews_page
from src.scrape import scrape_game_store_page

games = [
    594650,
    261550
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