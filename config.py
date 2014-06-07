#coding=utf-8
import os
from tornado.options import options, define

PROJDIR = os.path.abspath(os.path.dirname(__file__))


def init():
    define('debug', type=bool, default=True, help='application in debug mode?')
    define('port', type=int, default=8888,
           help='the port application listen to')
    define('token', type=str, default='', help='your wechat token')
    define('username', type=str, default='', help='your wechat username')
    define('simsimi_key', type=str, default='', help='simsimi api key')
    define('talkbot_brain_path', type=str, default='',
           help='talkbot brain file path')
    define('aiml_set', type=str, default=os.path.join(PROJDIR, 'aiml_set'),
           help='aiml set path')
    define('talkbot_properties', type=dict, default=dict(
        name=options.username,
        master=options.username,
        birthday='',
        gender='直男',
        city='安徽',
        os='OS X'
    ), help='talkbot properties')
    define('feed_url', type=str, default='', help='blog rss feed url')

