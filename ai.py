#coding=utf-8

import logging
import plugins


class AI(object):

    def __init__(self):
        self._plugin_modules = []
        self.load_plugins()

    def load_plugins(self):
        for name in plugins.__all__:
            try:
                __import__('plugins.%s' % name)
                self.add_plugin(getattr(plugins, name))
                logging.info('Plugin %s loaded success.' % name)
            except:
                logging.warning('Fail to load plugin %s' % name)

    def add_plugin(self, plugin):
        if not hasattr(plugin, 'test'):
            logging.error('Plugin %s has no method named test, ignore it')
            return False
        if not hasattr(plugin, 'respond'):
            logging.error('Plugin %s has no method named respond, ignore it')
            return False
        self._plugin_modules.append(plugin)
        return True

    def respond(self, data, msg=None):
        response = None
        for plugin in self._plugin_modules:
            try:
                if plugin.test(data, msg):
                    response = plugin.respond(data, msg)
            except:
                logging.warning('Plugin %s failed to respond.' % plugin.__name__)
                continue
            if response:
                break

        return response or u'呵呵'


bot = AI()

if __name__ == '__main__':
    print(bot.respond('hello'))
