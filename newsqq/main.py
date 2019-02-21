
from scrapy.cmdline import  execute

import sys
import os


base_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(base_dir)

execute(["scrapy","crawl","phoneContent_spider"])
#
# execute(["scrapy","crawl","Article"])