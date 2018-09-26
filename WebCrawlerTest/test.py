from __future__ import print_function
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import csv
import os
import time
import lxml
import urllib2
import re




url = "http://one.game/"

header = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}

resp = requests.get(url, headers=header)
content = resp.content

# print(content)

email = re.findall("([a-zA-Z0-9_.+-]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+)", content)
print(email)

# only_a_title = SoupStrainer('div', attrs={'class': 'info-wrapper--user-clicks'})
# soup = BeautifulSoup(content, "lxml", parse_only=only_a_title)
# subValues = soup.select('span[class="info-wrapper--clicks-text"]')
# print (soup)
#name = []
#print(subValues)
# num = 1;
# for i in subValues:
# 	if num%3 == 1:
# 		tmp = i.get_text()
# 		print(tmp[7:])
# 	if num%3 == 2:
# 		tmp = i.get_text()
# 		print(tmp[5:])
# 	num += 1
#	tmp = re.findall("\w+", i['href'])
#	del tmp[0]
#	print('-'.join(tmp))


#def getRatings(id):
#title = SoupStrainer('div', attrs = {'class': 'fixed_data'})
#soup = BeautifulSoup(content, "lxml", parse_only = title)
#values = soup.find('div', itemprop = 'ratingValue')
#subValues = soup.select('div[class="col_4"]')
#
#print(subValues)
#for i in subValues:
#	sub = re.findall("\d+", i.get_text())
#	if sub:
#		print('.'.join(sub))
#	else:
#		print(0)
#
#print(values['content'])
#
#def getDate(id):
#title = SoupStrainer('div', attrs = {'class': 'financial_data'})
#soup = BeautifulSoup(content, "lxml", parse_only = title)
#values = soup.find('small')
#
#print(values)



