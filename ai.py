#coding=utf-8

import logging
import plugins

plugin_modules = []
for name in plugins.__all__:
    try:
        __import__('plugins.%s' % name)
        plugin_modules.append(getattr(plugins, name))
        logging.info('plugin %s loaded success.' % name)
    except:
        logging.warning('load plugin %s failed.' % name)


def magic(data):
    response = ''
    for plugin in plugin_modules:
        try:
            if plugin.test(data):
                response = plugin.handle(data)
        except:
            continue
        if response:
            break

    return response or u'呵呵'

if __name__ == '__main__':
    print(magic('hello'))
