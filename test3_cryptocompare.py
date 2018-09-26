# coding: utf-8
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import csv
import os
import time
import lxml
import re
import urllib2

class Spider(object):
	def __init__(self):
		self.session = requests.session()
		self.targetUrl = None
		self.headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		}
		
	def getResponse(self, url=None):
		try:
			self.session.headers = self.headers
			self.targetUrl = url
			resp = self.session.get(self.targetUrl, headers = self.headers)
			return resp
		except Exception as e:
			print(e)
			
	def getName(self):
		url = 'https://www.cryptocompare.com/wallets/#/overview'
		try:
			content = self.getResponse(url).content
			title = SoupStrainer('script')
			soup = BeautifulSoup(content, "lxml", parse_only = title)
			print(content)
		except Exception as e:
			print(e)
		
#	def getID(self, url):
#		name = []
#		try:
#			content = self.getResponse(url).content
#			title = SoupStrainer('div', attrs = {'class': 'ico_list'})
#			soup = BeautifulSoup(content, "lxml", parse_only = title)
#			values = soup.select('a[class="name"]')
#			for i in values:
#				tmp = re.findall("\w+", i['href'])
#				del tmp[0]
#				name.append('-'.join(tmp))
#		except Exception as e:
#			print(e)
#		return name
#	
#	def getICOBenchLink(self, id):
#		url = 'https://icobench.com/ico/%s/' % id
#		try:
#			return url
#		except Exception as e:
#			print(e)
#			return ''
#	
#	def getRatings(self, id):
#		url = 'https://icobench.com/ico/%s/' % id
#		try:
#			content = self.getResponse(url).content
#			title = SoupStrainer('div', attrs = {'class': 'fixed_data'})
#			soup = BeautifulSoup(content, "lxml", parse_only = title)
#			rating = soup.find('div', itemprop = 'ratingValue')
#			subRating = soup.select('div[class="col_4"]')
#			ratings = []
#			ratings.append(rating['content'])
#			for i in subRating:
#				tmp = re.findall("\d+", i.get_text())
#				if tmp:
#					ratings.append('.'.join(tmp))
#				else:
#					ratings.append(0)
#			return ratings
#		except Exception as e:
#			print(e)
#			return ''
#	
#	def getDateStart(self, url):
#		start = []
#		try:
#			content = self.getResponse(url).content
#			title = SoupStrainer('div', attrs = {'class': 'ico_list'})
#			soup = BeautifulSoup(content, "lxml", parse_only = title)
#			date = soup.select('div[class="row"]')
#			num = 1;
#			for i in date:
#				if num%3 == 1:
#					tmp = i.get_text()
#					start.append(tmp[7:])
#				num += 1
#		except Exception as e:
#			print(e)
#			return ''
#		return start
#		
#	def getDateEnd(self, url):
#		end = []
#		try:
#			content = self.getResponse(url).content
#			title = SoupStrainer('div', attrs = {'class': 'ico_list'})
#			soup = BeautifulSoup(content, "lxml", parse_only = title)
#			date = soup.select('div[class="row"]')
#			num = 1;
#			for i in date:
#				if num%3 == 2:
#					tmp = i.get_text()
#					end.append(tmp[5:])
#				num += 1
#		except Exception as e:
#			print(e)
#			return ''
#		return end
#		
#	def dumpCSV(self):
#		path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'icoCoinRating.csv')
#		urls = ['https://icobench.com/icos?page={}'.format(str(i)) for i in range(34,133)]
#		with open(path, 'w') as f:
#			fieldnames = ['name','link', 'rating', 'ico_profile', 'team', 'vision', 'product', 'start', 'end']
#			wr = csv.DictWriter(f, fieldnames=fieldnames)
#			wr.writeheader()
#			i = 1
#			for url in urls:
#				ID = self.getID(url)
#				start = self.getDateStart(url)
#				end = self.getDateEnd(url)
#				for x, y, z in zip(ID, start, end):
#					print(i, x)
#					link = self.getICOBenchLink(x)
#					ratings = self.getRatings(x)
#					wr.writerow({'name': x, 'link': link, 'rating': ratings[0], 'ico_profile': ratings[1], 'team': ratings[2], 'vision': ratings[3], 'product': ratings[4], 'start': y, 'end': z})
#					i += 1

if __name__ == '__main__':
	spider = Spider()
	start = time.time()
	spider.getName()
	print(time.time() - start)
