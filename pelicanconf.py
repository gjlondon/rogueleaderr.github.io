#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'George J. London'
SITENAME = u'George J. London'
TAGLINE = 'Tinkerer/Thinkerer.'
SITEURL = 'http://rogueleaderr.github.io'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'


# can be useful in development, but set to False when you're ready to publish
RELATIVE_URLS = True

GITHUB_URL = 'http://github.com/rogueleaderr/'
DISQUS_SITENAME = "blog-rogueleaderr"
PDF_GENERATOR = False
REVERSE_CATEGORY_ORDER = True
DEFAULT_DATE = (2012, 3, 2, 14, 1, 1)

FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/%s.rss.xml'
THEME = './themes/svbtle'
OUTPUT_PATH = 'output'
PATH = 'content'

ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'

# Custom Home page
PAGE_DIR = 'pages'
PAGES_DIR = 'pages'

DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives'))
#PAGINATED_DIRECT_TEMPLATES = (('blog',))
TEMPLATE_PAGES = {'home.html': 'index.html',}

GENERATED_PAGES = ()
DISPLAY_PAGES_ON_MENU = True


# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS =  (('LinerNotes', 'http://www.linernotes.com'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True


SOCIAL = (('twitter', 'http://twitter.com/rogueleaderr'),)

# global metadata to all the contents
DEFAULT_METADATA = (('yeah', 'it is'),)

# # path-specific metadata
EXTRA_PATH_METADATA = {
     'extra/robots.txt': {'path': 'robots.txt'},
     'extra/.htaccess': {'path': '.htaccess'},

     }
#
# # static paths will be copied without parsing their contents
STATIC_PATHS = [
     'pictures',
     'extra/robots.txt',
     'themes/svbtle'
     ]
#
# custom page generated with a jinja2 template
#TEMPLATE_PAGES = {'pages/jinja2_template.html': 'jinja2_template.html'}
#
# # code blocks with line numbers
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}
#
# # foobar will not be used, because it's not in caps. All configuration keys
# # have to be in caps
# foobar = "barbaz"