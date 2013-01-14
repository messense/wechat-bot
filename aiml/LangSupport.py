#!/usr/bin/env python2
# -*- coding:utf-8 -*-

"""   LangSupport.py
提供对中文空格断字的支持。
    支持 GB 及 Unicode 。
    LangSupport 对象的 input 函数能在中文字之间添加空格。
    LangSupport 对象的 output 函数则是去除中文字之间的空格。
"""

from re import compile as re_compile
from string import join as str_join

findall_gb   = re_compile('[\x81-\xff][\x00-\xff]|[^\x81-\xff]+').findall
findall_utf8 = re_compile(u'[\u2e80-\uffff]|[^\u2e80-\uffff]+').findall
sub_gb       = re_compile('([\x81-\xff][\x00-\xff]) +(?=[\x81-\xff][\x00-\xff])').sub
sub_utf8     = re_compile(u'([\u2e80-\uffff]) +(?=[\u2e80-\uffff])').sub
sub_space    = re_compile(' +').sub

LangSupport = type('LangSupport', (object, ),
        {'__init__': lambda self, encoding = 'ISO8859-1': self.__setattr__('_encoding', encoding),
         '__call__': lambda self, s: self.input(s),
         'input'   : lambda self, s: s,
         'output' : lambda self, s: s } )

GBSupport = type('GBSupport', (LangSupport, ),
        {'input' : lambda self, s:
                str_join( findall_gb( type(s) == str and unicode(s, self._encoding) or s ) ),
         'output': lambda self, s:
                sub_space(' ', sub_gb(r'\1', ( type(s) == str and unicode(s, 'UTF-8') or s ).encode(self._encoding) ) ) } )

UnicodeSupport = type('UnicodeSupport', (LangSupport, ),
        {'input' : lambda self, s:
                str_join( findall_utf8( type(s) == str and unicode(s, self._encoding) or s ) ),
         'output': lambda self, s:
                sub_space(u' ', sub_utf8(r'\1', (type(s)==str and unicode(s,'UTF-8') or s) ) ) } 
                     )
