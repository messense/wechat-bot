#coding=utf-8

import os
import sys
sys.path.append('..')

import aiml

from tornado.options import options

class TalkBot(aiml.Kernel):
    def __init__(self):
        super(TalkBot, self).__init__()
        self.verbose(options.debug)
        if os.path.exists(options.talkbot_brain_path):
            self.bootstrap(brainFile=options.talkbot_brain_path)
        else:
            self.init_bot()
            self.saveBrain(options.talkbot_brain_path)

        for p in options.talkbot_properties:
            self.setBotPredicate(p, options.talkbot_properties[p])

    def init_bot(self):
        for f in os.listdir(options.aiml_set):
            if f.endswith('.aiml'):
                self.learn(os.path.join(options.aiml_set, f))

talkbot = TalkBot()

def test(data):
    return True

def handle(data):
    return talkbot.respond(data).encode('utf-8')
