# -*- coding: utf-8 -*-
# @Time    : 2017/7/9 上午10:09
# @Author  : yuzeyu
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#execute(["scrapy","crawl","jobbole"])
execute(["scrapy","crawl","zhihu"])