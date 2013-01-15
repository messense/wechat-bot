#coding=utf-8
import feedparser
from tornado.util import ObjectDict
from tornado.options import options

__name__ = 'feed'


def test(data, msg=None, bot=None):
    if not options.feed_url:
        return False
    if 'rss feed' in data or '博客更新' in data:
        return True
    return False


def respond(data, msg=None, bot=None):
    parser = feedparser.parse(options.feed_url)
    articles = []
    i = 0
    for entry in parser.entries:
        if i > 9:
            break
        article = ObjectDict()
        article.title = entry.title
        article.description = entry.description[0:100]
        article.url = entry.link
        article.picurl = ''
        articles.append(article)
        i += 1
    return articles
