from tuangou.utils.parser import FreeConfigParser


SITE_ROOT = os.path.dirname(os.path.realpath(__file__))


# firstly, load config file to initialize constant
SECTION = 'tuangou_spider'
cp = FreeConfigParser()
cp.read([os.path.join(SITE_ROOT, "conf/spider.cfg")])

CRAWLER_LEVEL = cp.getint(SECTION, "crawler_level", 0)