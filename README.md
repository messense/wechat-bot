# wechat-bot

A robot of wechat based on python

## How to run

First, clone the latest source from github:

```bash
$ git clone https://github.com/messense/wechat-bot.git
```

Then, install the required packages using pip:

```bash
$ [sudo] pip install -r requirements.txt
```

Create a text file named wechat.conf in the source code directory, write the configuration and save. For example:

```python
#coding=utf-8
debug = False
port = 8888
token = 'your token'
username = 'your username'
simsimi_key = ''
talkbot_brain_path = 'talkbot.brn'
```

Now, let's start the server:

```bash
$ python app.py
```

## License

wechat-bot published under the [MIT](http://opensource.org/licenses/MIT) license.

Copyright (c) 2013 messense

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.