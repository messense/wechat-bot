#coding=utf-8
import re
import requests

__name__ = 'ip'

ip_pattern = re.compile("((?:(?:25[0-5]|2[0-4]\d|[01]?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d?\d))", re.S)

def test(data, msg=None, bot=None):
    if ip_pattern.match(data):
        return True
    return False

def respond(data, msg=None, bot=None):
    m = ip_pattern.match(data)
    ip = m.group(1)
    res = requests.get("http://wap.ip138.com/ip_search.asp?ip=%s" % ip)
    result_pattern = re.compile(r".*<b>(.*)<\/b>.*", re.I | re.S | re.M)
    m = result_pattern.match(res.text)
    if m:
        result = m.group(1)
        return result.encode('utf-8')
    return u'查询 IP 地址 %s 失败' % ip

if __name__ == '__main__':
    print(respond("192.168.1.1"))
