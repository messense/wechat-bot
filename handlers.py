#coding=utf-8
import logging
import wechat
import ai

from hashlib import sha1
from tornado import web
from tornado.options import options


class WechatHandler(web.RequestHandler):

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

        tmparr = [options.token, timestamp, nonce].sort()
        tmpstr = ''.join(tmparr)
        tmpstr = sha1(tmpstr).hexdigest()

        if tmpstr == signature:
            return True
        else:
            return False

    def post(self):
        self.set_header("Content-Type", "application/xml;charset=utf-8")
        body = self.request.body
        msg = wechat.parse_user_msg(body)
        if not msg:
            return
        if msg.type == wechat.MSG_TYPE_TEXT:
            text = ai.magic(msg.content)
            reply = wechat.reply_with_text(msg.fromuser, text)
            self.write(reply)
        elif msg.type == wechat.MSG_TYPE_LOCATION:
            pass
        else:
            pass
        

handlers = [
    ('/', WechatHandler),
]
