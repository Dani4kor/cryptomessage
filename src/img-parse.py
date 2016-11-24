from bs4 import BeautifulSoup
from urllib2 import urlopen
import time
from datetime import timedelta
import pprint

response = urlopen('http://spacetelescope.org/images/')

soup = BeautifulSoup(response, 'html.parser')
t = [x.get('src') for x in soup.findAll('img')]
pprint.pprint(t, width=1)