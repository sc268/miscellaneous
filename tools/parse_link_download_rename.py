"""
    Copyright (c) 2016 Sean Chang, seanchang.stat@gmail.com
    
    Parse pdf links on a course page, download and rename according to the lecture title.

"""

import urllib
import re
from bs4 import BeautifulSoup

url_source = "http://web.stanford.edu/class/ee378a/"
url = url_source + "material.html"
response = urllib.urlopen(url)
soup = BeautifulSoup(response)
urls = []
names = []


# extract links
match = re.compile('lecture[0-9]+\.(pdf)')
for link in soup.findAll('a'):
    try:
        href = link['href']
        if re.search(match, href):
            href = url_source + href
            urls.append(href)
    except KeyError:
        pass


# extract titles
dat = soup.findAll(text=re.compile('Lecture\s([0-9]+):'))
print dat

for text in dat:
    text = re.sub(r"(. \r\n)|:|(.\r\n)|(.$)|'|,|(\.$)", "", text)
    print text
    names.append(text+'.pdf')


# save files
for i in xrange(len(urls)):
    try:
        print names[i]
        print urls[i]
        file = urllib.URLopener()
        file.retrieve(urls[i], names[i])
    except KeyError:
        print 'title or url does not exist'
