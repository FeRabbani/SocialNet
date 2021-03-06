# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
  
import os
import random
from scrapy import signals
from scrapy.conf import settings


class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        ua = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')
