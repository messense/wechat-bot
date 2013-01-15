#coding=utf-8
import requests
from xml.etree import ElementTree
from tornado.util import ObjectDict

__name__ = 'oschina'


def test(data, msg=None, bot=None):
    if ('oschina' in data or '开源中国' in data) and '最新' in data and '新闻' in data:
        return True
    return False

def respond(data, msg=None, bot=None):
    headers = {
        'Host' : 'www.oschina.net',
        'Connection' : 'Keep-Alive',
        'User-Agent' : 'OSChina.NET/1.7.4_1/Android/4.1/Nexus S/12345678'
    }
    res = requests.get("http://www.oschina.net/action/api/news_list",
                       headers=headers)
    parser = ElementTree.fromstring(res.content)
    news_list = parser.find('newslist')
    articles = []
    i = 0
    for news in news_list.iter('news'):
        if i > 9:
            break
        article = ObjectDict()
        article.title = news.find('title').text
        article.description = article.title
        article.url = "http://www.oschina.net/news/%s" % news.find('id').text
        article.picurl = ''
        articles.append(article)
        i += 1

    return articles
