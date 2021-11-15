import time
import datetime
import os
import requests
import threading
import urllib.request
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.files import File

from .models import RssLinks, News, Team, Player
from apscheduler.schedulers.background import BackgroundScheduler


def get_image_name(link):
    return link[link.rindex('/') + 1:]


def get_http_response(url):
    tries = 0
    while tries < 5:
        response = requests.get(url)
        if response.status_code:
            break
        tries += 1
    if tries == 5:
        return
    return response


def set_news(rss_link, date_time):
    response = get_http_response(rss_link)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html)
    title = soup.find('h1').get_text()
    team_labels = []
    player_labels = []
    news_div = soup.find('div', class_='news-page--news-text')
    p_elements = news_div.find_all('p')
    news_text = ''
    for p in p_elements:
        news_text += p.get_text()
    news_image_url = news_div.find('img')['src']
    image_path = os.path.join(settings.BASE_DIR, 'Media', 'news_images', get_image_name(news_image_url))
    urllib.request.urlretrieve(news_image_url, image_path)
    tags = soup.find('div', class_='tags-list').find_all('a')
    for tag in tags:
        tag = tag.text
        team = Team.objects.filter(name=tag)
        if len(team) == 0:
            player = Player.objects.filter(name=tag)
            if len(player) != 0:
                player_labels.append(player[0])
        else:
            team_labels.append(team[0])
    news = News.objects.create(news_date=date_time, title=title, text=news_text, is_hot=False)
    news.image.save(get_image_name(news_image_url), File(open(image_path, 'rb')))
    news.team_label.set(team_labels)
    news.players_label.set(player_labels)
    news.save()


def set_rss_links_news():
    response = get_http_response('https://www.varzesh3.com/rss/foreignFootball').text
    rss_xml = ET.fromstring(response)
    rss_link = None
    does_news_exists = True
    for tag in rss_xml[0]:
        if tag.tag == 'item':
            for item_child in tag:
                if item_child.tag == 'link':
                    rss_link = item_child.text
                    try:
                        same_rss_link = RssLinks.objects.get(rss_link=rss_link)
                    except RssLinks.DoesNotExist:
                        rss_link_record = RssLinks()
                        rss_link_record.rss_link = rss_link
                        rss_link_record.save()
                        does_news_exists = False
                if item_child.tag == 'pubDate':
                    if not does_news_exists:
                        date_time = datetime.datetime.fromisoformat(item_child.text)
                        set_news(rss_link, date_time)
        does_news_exists = True

scheduler = BackgroundScheduler()
job = scheduler.add_job(set_rss_links_news, 'interval', minutes=1)
scheduler.start()
