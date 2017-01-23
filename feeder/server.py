"""feeder server.py."""
from flask import Flask, render_template, abort

import feedparser


APP = Flask(__name__)


@APP.errorhandler(404)
def page_not_found(error):
    """page not found."""
    return render_template('404.html', error=error), 404


FEED_URL_DICT = {
    'infoq': 'http://www.infoq.com/cn/feed',
    'sspai': 'http://sspai.com/feed',
    'coolshell': 'http://coolshell.cn/feed',
    'keakon': 'https://www.keakon.net/feed',
    'zhouyichu': 'http://zhouyichu.com/atom.xml',
    'aisk': 'http://aisk.me/rss/',
    'seanlook': 'http://seanlook.com/atom.xml',
    'selfboot': 'http://selfboot.cn/atom.xml',
    'wulfric': 'http://wulfric.me/feed.xml',
    'imququ': 'https://imququ.com/rss.html',
    'colorfulkoala': 'http://feed.cnblogs.com/blog/u/113765/rss',
    'hi-linux': 'http://www.hi-linux.com/atom.xml',
    'lcbk': 'http://lcbk.net/feed/',
    'linuxzen': 'https://www.linuxzen.com/feeds/all.atom.xml',
    'oilbeater': 'http://oilbeater.com/atom.xml',
    'droidyue': 'http://droidyue.com/atom.xml',
    'wklken': 'http://www.wklken.me/feed.xml',
    'cyrusin': 'https://cyrusin.github.io/atom.xml',
    'kingname': 'http://kingname.info/atom.xml',
    'the5fire': 'https://www.the5fire.com/rss/',
    'ruanyifeng': 'http://www.ruanyifeng.com/blog/atom.xml',
    'liaoxuefeng': 'http://www.liaoxuefeng.com/feed',
    'xclient': 'http://xclient.info/feed/',
    'aotu': 'https://aotu.io/atom.xml',
    'ifanr': 'http://www.ifanr.com/feed',
    'huxiu': 'https://www.huxiu.com/rss/0.xml',
    'v2ex': 'https://www.v2ex.com/index.xml',
    '91ri': 'http://www.91ri.org/feed',
    'xitu': 'https://gold.xitu.io/rss',
    'codingpy': 'http://codingpy.com/feed/',
    'rowkey': 'http://www.rowkey.me/atom.xml'
}


@APP.route('/')
def homepage():
    """Home."""
    data = FEED_URL_DICT.keys()
    return render_template('home.html', data=data)


@APP.route('/<urlname>')
def infoq_subscription(urlname):
    """infoq."""
    try:
        url = FEED_URL_DICT[urlname]
    except KeyError:
        abort(404)

    feed = feedparser.parse(url)
    return render_template('content.html', data=feed)


if __name__ == '__main__':
    APP.run(debug=True)
