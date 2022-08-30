import uuid
from datetime import datetime
import os

from dotenv import load_dotenv
from bs4 import BeautifulSoup
import mysql.connector
import requests
from selenium import webdriver
import unicodedata
from pprint import pprint

load_dotenv()

HOST_YA = 'https://market.yandex.ru'
URL_YA = 'https://market.yandex.ru/partners/news'
URL_OZON = 'https://seller.ozon.ru/news'
HEADERS = {
    'accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
               'image/avif,image/webp,image/apng,*/*;q=0.8,application/'
               'signed-exchange;v=b3;q=0.9'),
    'user-agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                   '537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')
}

driver = webdriver.Chrome()


class News:

    def __init__(self, title, description, url, tags, pub_date, source):
        self.uid = uuid.uuid4()
        self.title = title
        self.description = description
        self.url = url
        self.tags = tags
        self.pub_date = pub_date
        self.source = source

    @staticmethod
    def get_json(news):
        return dict(
            title=news.title,
            description=news.description,
            url=news.url,
            tags=news.tags,
            pub_date=news.pub_date.isoformat(),
            source=news.source
        )


def get_html(url, params=''):
    response = requests.get(url, headers=HEADERS, params=params)
    return response


def get_ya_tags_context(url, params=''):
    link = requests.get(
        url=url,
        headers=HEADERS,
        params=params
    )
    soup = BeautifulSoup(link.text, 'html.parser')
    tags = [
        tag for tag in soup.find(
            'div', class_='news-info__tags'
        ).get_text().split('#')[1:]
    ]
    return tags


def get_ya_context(html):
    soup = BeautifulSoup(html, 'html.parser')
    news = soup.find_all('div', class_='news-list__item', limit=10)
    return list(
        map(
            lambda item: News(
                title=item.find(
                    'div', class_='news-list__item-header'
                ).get_text(strip=True),
                description=item.find(
                    'div', class_='news-list__item-description'
                ).find('p').get_text(strip=True),
                url=HOST_YA + item.find('a', class_='link').get('href'),
                tags=get_ya_tags_context(
                    HOST_YA + item.find('a', class_='link').get('href')
                ),
                pub_date=datetime.fromisoformat(item.find(
                    'div', class_='news-list__item-meta'
                ).find('time').get('datetime')),
                source='Yandex'
            ),
            news
        )
    )


def fetch_data(url):
    driver.get(url=url)
    return driver.page_source


def enc_text(text):
    return str.strip(unicodedata.normalize('NFKD', text))


def fetch_ozon():
    months = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5,
        'июня': 6, 'июля': 7, 'августа': 8, 'сентября': 9, 'октября': 10,
        'ноября': 11, 'декабря': 12
    }

    def get_date(val, year):
        data = val.split(' ')
        return f'{year}-{months[data[1]]}-{data[0]}'

    data = fetch_data(URL_OZON)
    if data:
        soup = BeautifulSoup(data, 'lxml')
        news = list(map(lambda item: item.next, soup.find_all(
            'div', class_='news-card'
        )))
        return list(
            map(
                lambda value: News(
                    title=enc_text(
                        value.find('h3', class_='news-card__title').text
                    ),
                    description=enc_text(
                        value.find('h3', class_='news-card__title').text
                    ),
                    url=enc_text(
                        value.find('a').get('href')
                    ),
                    tags=list(map(
                        lambda tag: enc_text(tag.text), value.find_all(
                            'div', class_='news-card__mark'
                        ))),
                    pub_date=datetime.strptime(
                        get_date(enc_text(value.find(
                            'span', class_='news-card__date'
                        ).text), 2022), '%Y-%m-%d'),
                    source='Ozon'
                ),
                news
            )
        )


def fill_db(data):
    db = mysql.connector.connect(
        host=os.getenv('DB_HOST', default='localhost'),
        user=os.getenv('MYSQL_USER', default='root'),
        password=os.getenv('MYSQL_PASSWORD', default='root'),
        database=os.getenv('DB_NAME', default='voxweb'),
    )
    tags = dict()
    for row in data:
        tags.update({tag: uuid.uuid4().hex for tag in row.tags})

    data_constraint = []
    for row in data:
        data_constraint += (list(zip(
            [row.uid.hex] * len(row.tags),
            [tags[tag] for tag in row.tags]
        )))

    cursor = db.cursor()

    cursor.executemany(
        "INSERT INTO news_service_news"
        "(uid, title, description, url, pub_date, source)"
        "VALUES (%s, %s, %s, %s, %s, %s);",
        list(map(lambda news: (
            news.uid.hex,
            news.title,
            news.description,
            news.url,
            news.pub_date,
            news.source
        ), data))
    )

    cursor.executemany(
        "INSERT INTO news_service_tag(uid, name) VALUES (%s, %s)",
        [(tags[tag], tag) for tag in tags]
    )

    cursor.executemany(
        "INSERT INTO news_service_news_tags(news_id, tag_id) VALUES (%s, %s)",
        data_constraint
    )

    db.commit()
    cursor.close()
    db.close()


if __name__ == "__main__":
    html = get_html(URL_YA)
    result = [*get_ya_context(html.text), *fetch_ozon()]
    fill_db(data=result)
    driver.close()
    driver.quit()
