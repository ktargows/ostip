#!/usr/bin/env python
import requests
import logging
import itertools
import re

LOG = logging.getLogger(__name__)


class GetHttp:

    # "config": {
    #     "url": "https://sslbl.abuse.ch/blacklist/sslipblacklist.csv",
    #     "ignore_regex": "^#",
    #     "user_agent": "OSTIP",
    #     "referer": null,
    #     "timeout": 20,
    #     "verify_cert": true
    # }

    def __init__(self, config):
        self.url = config.get('url')
        self.ignore_regex = config.get('ignore_regex')
        self.user_agent = config.get('user_agent', 'OSTIP')
        self.referer = config.get('referer')
        self.timeout = config.get('timeout', 20)
        self.verify_cert = config.get('verify_cert', True)

        if self.ignore_regex:
            self.ignore_regex = re.compile(self.ignore_regex)

    def get(self):
        rkwargs = dict(
            stream=True,
            verify=self.verify_cert,
            timeout=self.timeout,
            headers={ 'User-Agent': self.user_agent or 'OSTIP' }
        )

        if self.referer:
            rkwargs['headers']['referer'] = self.referer

        r = requests.get(
            self.url,
            **rkwargs
        )

        try:
            r.raise_for_status()
        except:
            LOG.debug('%s - exception in request: %s %s',
                      self.url, r.status_code, r.content)
            raise

        result = r.iter_lines()
        if self.ignore_regex:
            result = itertools.ifilter(
                lambda x: self.ignore_regex.match(x) is None,
                result
            )

        return result