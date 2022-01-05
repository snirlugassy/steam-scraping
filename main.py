import json

from src.scrape import scrape_game_reviews_page
from src.scrape import scrape_game_store_page

games = [
    {'id': 261550, 'name': 'Mount__Blade_II_Bannerlord'}
]

data = []
for game in games:
    steam_game = scrape_game_store_page(game['id'])
    print(steam_game)

    steam_reviews = scrape_game_reviews_page(game['id'], review_limit=100)
    print(steam_reviews)

    data.append({
        'game': steam_game.to_dict(),
        'reviews': [r.to_dict() for r in steam_reviews]
    })

with open('data.json', 'w') as f:
    json.dump(data, f)