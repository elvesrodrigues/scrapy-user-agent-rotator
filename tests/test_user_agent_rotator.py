import unittest

from scrapy.http import Request
from scrapy.spiders import Spider
from scrapy.utils.test import get_crawler

from user_agent_rotator import RotateUserAgentMiddleware

class TestUserAgentRotator(unittest.TestCase):
    def test_rotation(self):
        '''Tests whether user-agents are being rotated'''
        
        user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
            'Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        ]

        min_user_agent_usage = 1
        max_user_agent_usage = 100

        crawler = get_crawler(spidercls=Spider, settings_dict={'ROTATE_USER_AGENT_ENABLED': True , 'USER_AGENTS': user_agents, 'MIN_USER_AGENT_USAGE': min_user_agent_usage, 'MAX_USER_AGENT_USAGE': max_user_agent_usage})
        
        spider = crawler._create_spider('foo')
        middleware = RotateUserAgentMiddleware.from_crawler(crawler)
        
        urls = ['http://scrapytest.org/'] * 100000

        user_agent_usage = 0
        
        last_ua = ''
        curr_ua = ''

        for url in urls:
            req = Request(url)
            middleware.process_request(req, spider)

            curr_ua = req.headers['User-Agent']

            if curr_ua != last_ua and user_agent_usage:
                self.assertTrue(min_user_agent_usage <= user_agent_usage <= max_user_agent_usage)
                user_agent_usage = 0

            last_ua = curr_ua        
            user_agent_usage += 1

        self.assertTrue(user_agent_usage <= max_user_agent_usage)