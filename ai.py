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


def magic(data, bot=None):
    response = ''
    for plugin in plugin_modules:
        try:
            if plugin.test(data, bot):
                response = plugin.handle(data, bot)
        except:
            continue
        if response:
            break

    return response or 'I don\'t understand.'

if __name__ == '__main__':
    print(magic('hello'))
