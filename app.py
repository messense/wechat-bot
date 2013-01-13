#!/usr/bin/env python
#coding=utf-8
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

import os
import logging

from tornado import web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import options, define
from tornado.options import parse_command_line

PROJDIR = os.path.abspath(os.path.dirname(__file__))

define('debug', type=bool, default=True, help='application in debug mode?')
define('port', type=int, default=8888, help='the port application listen to')
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


def parse_config_file(path):
    if not path or not os.path.exists(path):
        return
    config = {}
    exec(compile(open(path).read(), path, 'exec'), config, config)
    for name in config:
        if name in options:
            options[name].set(config[name])
        else:
            define(name, config[name])


class Application(web.Application):

    def __init__(self):
        from handlers import handlers
        settings = dict(
            debug=options.debug,
            autoescape=None
        )
        super(Application, self).__init__(handlers, **settings)


def main():
    if options.debug:
        define('settings', '%s/wechat.conf' % PROJDIR)
    else:
        define('settings', '')
    parse_command_line()
    parse_config_file(options.settings)

    logging.info('Starting server at port %s' % options.port)

    server = HTTPServer(Application(), xheaders=True)
    server.listen(int(options.port))
    IOLoop.instance().start()

if __name__ == '__main__':
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting app")
