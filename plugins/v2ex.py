#coding=utf-8
import requests
from tornado.escape import json_decode
from tornado.util import ObjectDict


def test(data):
    if 'v2ex' in data and '话题' in data and '最新' in data:
        return True
    return False


def respond(data):
    res = requests.get("http://www.v2ex.com/api/topics/latest.json")
    topics = json_decode(res.text)
    articles = []
    i = 0
    while i < 5:
        article = ObjectDict()
        article.title = topics[i]['title']
        article.url = topics[i]['url']
        article.picurl = 'http://openoceans.de/img/v2ex_logo_uranium.png'
        article.description = topics[i]['content_rendered'][0:100]
        articles.append(article)
        i += 1
    return articles
