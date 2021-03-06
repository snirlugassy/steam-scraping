import time
import re

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

from src.game import SteamGame
from src.review import SteamReview


driver_path = '/home/snirlugassy/Documents/School/Gorem/HW2/geckodriver'

USE_BROWSER = 'safari'

def store_page_url(game_id):
    return f'https://store.steampowered.com/app/{game_id}/'

def reviews_page_url(game_id):
    return f'https://steamcommunity.com/app/{game_id}/reviews/?p=1&browsefilter=toprated'

def get_firefox_driver():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')

    return webdriver.Firefox(options=options, executable_path=driver_path)

def get_safari_driver():
    # For MacOS: Run `safaridriver --enable` in the terminal before using Safari Driver
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')

    return webdriver.Safari(options=Options)

def get_driver():
    if USE_BROWSER == 'firefox':
        return get_firefox_driver()
    elif USE_BROWSER == 'safari':
        return get_safari_driver()

def scrape_game_store_page(game_id):
    driver = get_driver()
    driver.get(store_page_url(game_id))

    try:
        select_year = Select(driver.find_element_by_id('ageYear'))
        select_year.select_by_value('1990')
        btn = driver.find_element_by_id('view_product_page_btn')
        btn.click()
        time.sleep(3)
    except:
        pass

    soup = BeautifulSoup(driver.page_source, 'html')

    game_title = soup.find('div', id='appHubAppName').text.strip()
    price = soup.find('div', class_='game_purchase_price').text.strip()
    video_src = soup.find('video').attrs.get('src')
    review_count = int(soup.find('meta', itemprop='reviewCount')['content'])
    rating = int(soup.find('meta', itemprop='ratingValue')['content'])
    release_date = soup.find('div', class_='release_date').find('div', class_='date').text.strip()
    game_description = soup.find('div', class_='game_description_snippet').text.strip()
    game_image = soup.find('img', class_='game_header_image_full')['src']

    dev_info = {}
    for dev_row in soup.find(class_='glance_ctn').find_all(class_='dev_row'):
        dev_info[dev_row.find(class_='subtitle').text.replace(':','')] = dev_row.find(class_='summary').text.strip()

    tags = []
    for tag in soup.find(class_='glance_tags popular_tags').find_all('a'):
        if 'display: none' not in tag['style']:
            tags.append(tag.text.strip())

    features = []
    for spec in soup.find('div', id='category_block').find_all(class_='game_area_details_specs_ctn'):
        features.append(spec.find(class_='label').text.strip())

    min_sys_req = []
    min_sys_req_soup = soup.find('div', class_='game_area_sys_req').find('div', class_='game_area_sys_req_leftCol')
    if min_sys_req_soup:
        for req in min_sys_req_soup.find('ul', class_='bb_ul').find_all('li'):
            min_sys_req.append(req.text.strip())

    rec_sys_req = []
    rec_sys_req_soup = soup.find('div', class_='game_area_sys_req').find('div', class_='game_area_sys_req_rightCol')
    if rec_sys_req_soup:
        for req in rec_sys_req_soup.find('ul', class_='bb_ul').find_all('li'):
            rec_sys_req.append(req.text.strip())

    driver.close()

    return SteamGame(
        title=game_title,
        description=game_description,
        price=price,
        developer=dev_info.get('Developer'),
        publisher=dev_info.get('Publisher'),
        rating=rating,
        review_count=review_count,
        release_date=release_date,
        features=features,
        tags=tags,
        img=game_image,
        video_src=video_src,
        min_sys_req=min_sys_req,
        rec_sys_req=rec_sys_req
    )

def scrape_game_reviews_page(game_id, review_limit):
    driver = get_driver()
    driver.get(reviews_page_url(game_id))

    try:
        btn = driver.find_element_by_id('age_gate_btn_continue')
        btn.click()
        time.sleep(3)
    except:
        pass

    review_cards = driver.find_elements_by_class_name('apphub_Card')

    attempts = 0
    last_count = 0
    while len(review_cards) < review_limit:
        if last_count == len(review_cards):
            attempts += 1
        else:
            attempts = 0
        if attempts > 10:
            break
        last_count = len(review_cards)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        review_cards = driver.find_elements_by_class_name('apphub_Card')

    soup = BeautifulSoup(driver.page_source)
    cards = soup.find_all('div', class_='apphub_Card')

    reviews = []
    for card in cards:
        recommendation = card.find('div', class_='reviewInfo').find(class_='title').text.strip()

        helpful = card.find('div', class_='found_helpful')

        for br in helpful.find_all('br'):
            br.replaceWith(', ')

        helpful_text = []
        for _child in helpful.children:
            if isinstance(_child, str):
                helpful_text.append(_child)

        helpful_text = ''.join(helpful_text).strip()

        review_total_rewards = int(card.find(class_='review_award_aggregated').text.replace(',','').strip())

        review_text = []
        for _child in card.find('div', class_='apphub_CardTextContent').children:
            if isinstance(_child, str):
                review_text.append(_child)
        review_text = ''.join(review_text).strip()

        hrs_on_record = card.find('div', class_='reviewInfo').find(class_='hours').text.strip()
        hrs_on_record = re.search('[0-9.]+', hrs_on_record)
        if hrs_on_record:
            hrs_on_record = float(hrs_on_record.group())

        reviews.append(SteamReview(
            text=review_text,
            helpful=helpful_text,
            recommendation=recommendation,
            rewards=review_total_rewards,
            hrs_on_record=hrs_on_record
        ))
    
    driver.close()

    return reviews
