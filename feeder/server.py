# coding: utf-8
"""feeder server.py."""
import ujson
import optparse

from flask import Flask, render_template, abort

import feedparser

from extensions.redis import KVSTORE


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
    'dongwm': 'http://www.dongwm.com/atom.xml',
    'rowkey': 'http://www.rowkey.me/atom.xml',
    'sec-wiki': 'https://www.sec-wiki.com/news/rss'
}


@APP.route('/')
def homepage():
    """Home."""
    sidemenus = FEED_URL_DICT.keys()
    return render_template('home.html', sidemenus=sidemenus)


@APP.route('/<urlname>')
def infoq_subscription(urlname):
    """infoq."""
    try:
        url = FEED_URL_DICT[urlname]
    except KeyError:
        abort(404)

    data = KVSTORE.get(url)
    if data:
        feed = ujson.loads(data)
    else:
        feed = feedparser.parse(url)

        data = ujson.dumps(feed)

        timeout = 3600 * 12
        KVSTORE.set(url, data, timeout)

    sidemenus = FEED_URL_DICT.keys()
    return render_template('content.html', data=feed, sidemenus=sidemenus)


def flaskrun(default_host="127.0.0.1", default_port="5000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app [default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app [default %s]" % default_port,
                      default=default_port)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile",
                      action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        APP.config['PROFILE'] = True
        APP.wsgi_app = ProfilerMiddleware(APP.wsgi_app, restrictions=[30])
        options.debug = True

    APP.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )

if __name__ == '__main__':
    flaskrun()
