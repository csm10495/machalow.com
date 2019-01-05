#!/usr/bin/env python3
# Quick script to try to turn the hfqfb rss into one with images.
# Author: Charles Machalow

import copy
import re
from six.moves import urllib
import xml.etree.ElementTree as ET

COUPON_IMAGE_FIND_REGEX = rb'img src\=\"(.?\/coupons\/.*?)\"'
URL_PREFIX = rb'http://www.hfqpdb.com'

class RSS(object):
    def __init__(self):
        self.rssText = self.getSanitizedRssText()
        self.rssXml = ET.fromstring(self.rssText)

    @classmethod
    def getSanitizedRssText(cls):
        txt = urllib.request.urlopen(r"http://www.hfqpdb.com/feed/").read()
        txt = txt.replace(b'&rdquo', b'&quot') # Fix incorrect unicode stuff
        return txt

    def getRssXmlWithImages(self):
        workingXml = copy.deepcopy(self.rssXml)
        channel = workingXml.find('channel')
        items = channel.findall('item')
        for item in items:
            itemUrl = item.find('link').text
            imageUrl = self.getCouponImageUrlFromUrl(itemUrl)
            if imageUrl:
                description = item.find('description')
                description.text = '<img src="{img}" title="{desc}" />'.format(img=imageUrl.decode(), desc=description.text)

        return workingXml

    @classmethod
    def getCouponImageUrlFromUrl(cls, url):
        txt = urllib.request.urlopen(url).read()
        try:
            foundUrl = re.findall(COUPON_IMAGE_FIND_REGEX, txt)[0]
        except IndexError:
            return None
        return URL_PREFIX + foundUrl


if __name__ == '__main__':
    rss = RSS()
    print (rss.getRssXmlWithImages())



