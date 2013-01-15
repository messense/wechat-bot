#coding=utf-8
import logging
import wechat

from hashlib import sha1
from tornado import web
from tornado.options import options
from ai import bot


class WechatHandler(web.RequestHandler):
    def get_error_html(self, status_code, **kwargs):
        self.set_header("Content-Type", "application/xml;charset=utf-8")
        try:
            if self.touser and self.fromuser:
                reply = wechat.reply_with_text(self.touser, self.fromuser,
                                               '矮油，系统出错了，没法回答你了。')
                self.write(reply)
                return
        except:
            pass

    def get(self):
        echostr = self.get_argument('echostr', '')
        if self.check_signature():
            self.write(echostr)
            logging.info("Signature check success.")
        else:
            logging.warning("Signature check failed.")

    def check_signature(self):
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')

        tmparr = [options.token, timestamp, nonce]
        tmparr.sort()
        tmpstr = ''.join(tmparr)
        tmpstr = sha1(tmpstr).hexdigest()

        if tmpstr == signature:
            return True
        else:
            return False

    def post(self):
        if not self.check_signature():
            logging.warning("Signature check failed.")
            return

        self.set_header("Content-Type", "application/xml;charset=utf-8")
        body = self.request.body
        msg = wechat.parse_user_msg(body)
        if not msg:
            logging.info('Empty message, ignored')
            return

        self.touser = msg.touser
        self.fromuser = msg.fromuser

        if msg.type == wechat.MSG_TYPE_TEXT:
            if options.debug:
                logging.info('message type text from %s', msg.fromuser)

            response = bot.respond(msg.content, msg)
            reply = wechat.generate_reply(msg.touser, msg.fromuser, response)
            self.write(reply)

            if options.debug:
                logging.info('Replied to %s with "%s"', msg.fromuser, response)
        elif msg.type == wechat.MSG_TYPE_LOCATION:
            if options.debug:
                logging.info('message type location from %s', msg.fromuser)
        elif msg.type == wechat.MSG_TYPE_IMAGE:
            if options.debug:
                logging.info('message type image from %s', msg.fromuser)
        else:
            logging.info('message type unknown')


handlers = [
    ('/', WechatHandler),
]
