# coding=utf-8
import logging

from tornado import web
from tornado.options import options
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from ai import AI


class WechatHandler(web.RequestHandler):

    def get(self):
        echostr = self.get_argument('echostr', '')
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        try:
            check_signature(options.token, signature, timestamp, nonce)
        except InvalidSignatureException:
            logging.warning("Signature check failed.")
        else:
            logging.info("Signature check success.")
            self.write(echostr)

    def post(self):
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        try:
            check_signature(options.token, signature, timestamp, nonce)
        except InvalidSignatureException:
            logging.warning("Signature check failed.")
            return

        self.set_header("Content-Type", "application/xml;charset=utf-8")
        body = self.request.body
        msg = parse_message(body)
        if not msg:
            logging.info('Empty message, ignored')
            return

        # new bot
        bot = AI(msg)

        if msg.type == 'text':
            if options.debug:
                logging.info('message type text from %s', msg.source)

            response = bot.respond(msg.content, msg)
            reply = create_reply(response, msg, render=True)
            self.write(reply)

            if options.debug:
                logging.info('Replied to %s with "%s"', msg.source, response)
        elif msg.type == 'location':
            if options.debug:
                logging.info('message type location from %s', msg.source)
        elif msg.type == 'image':
            if options.debug:
                logging.info('message type image from %s', msg.source)
        else:
            logging.info('message type unknown')


handlers = [
    ('/', WechatHandler),
]
