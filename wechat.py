#coding=utf-8
import time
from tornado.util import ObjectDict
from tornado.options import options
from xml.etree import ElementTree

MSG_TYPE_TEXT = u'text'
MSG_TYPE_LOCATION = u'location'
MSG_TYPE_IMAGE = u'image'


def decode(s):
    if isinstance(s, str):
        s = s.decode('utf-8')
    return s


def parse_user_msg(xml):
    if not xml:
        return None
    parser = ElementTree.fromstring(xml)
    msg_type = decode(parser.find('MsgType').text)
    touser = decode(parser.find('ToUserName').text)
    fromuser = decode(parser.find('FromUserName').text)
    create_at = int(parser.find('CreateTime').text)
    msg = ObjectDict(
        type=msg_type,
        touser=touser,
        fromuser=fromuser,
        time=create_at
    )
    if msg_type == MSG_TYPE_TEXT:
        msg.content = decode(parser.find('Content').text)
    elif msg_type == MSG_TYPE_LOCATION:
        msg.location_x = decode(parser.find('Location_X').text)
        msg.location_y = decode(parser.find('Location_Y').text)
        msg.scale = int(parser.find('Scale').text)
        msg.label = decode(parser.find('Label').text)
    elif msg_type == MSG_TYPE_IMAGE:
        msg.picurl = decode(parser.find('PicUrl').text)

    return msg


def reply_with_text(fromuser, touser, text):
    tpl = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <FuncFlag>0</FuncFlag>
    </xml>
    """

    timestamp = int(time.time())
    return tpl % (touser, fromuser, timestamp, MSG_TYPE_TEXT, text)


def reply_with_articles(fromuser, touser, articles, text=''):
    tpl = """<xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    <ArticleCount>%s</ArticleCount>
    <Articles>%s</Articles>
    <FuncFlag>0</FuncFlag>
    </xml>
    """
    itemtpl = """<item>
    <Title><![CDATA[%s]]></Title>
    <Description><![CDATA[%s]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
    </item>
    """
    
    timestamp = int(time.time())
    items = []
    if not isinstance(articles, list):
        articles = [articles]
    count = len(articles)
    for article in articles:
        item = itemtpl % (article['title'], article['description'],
                          article['picurl'], article['url'])
        items.append(item)
    article_str = '\n'.join(items)

    return tpl % (touser, fromuser, timestamp,
                  text, count, article_str)
