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
			resp = self.session.get(self.targetUrl, headers=self.headers)
			return resp
		except Exception as e:
			print(e)
		
	def getVolume(self):
		url = 'https://api.coinmarketcap.com/v1/ticker/?limit=2000'
		try:
			resp = self.getResponse(url)
		except Exception as e:
			print(e)
		return resp.json()

	def getWebSite(self, id):
		url = 'https://coinmarketcap.com/currencies/%s/' % id
		try:
			html = self.getResponse(url).content
			only_a_title = SoupStrainer('ul', attrs={'class': 'list-unstyled'})
			soup = BeautifulSoup(html, "lxml", parse_only=only_a_title)
			links = soup.select('span[title="Website"] ~ a')
			r = []
			for x in links:
				r.append(x['href'])
			return ' , '.join(r)
		except Exception as e:
			print(e)
			return ''
	
	#非小号网址
	def getFeiXiaohaoLink(self, id):
		url = 'https://www.feixiaohao.com/currencies/%s/' % id
		try:
			return url
		except Exception as e:
			print(e)
			return ''
			
	#发行日期
	def getDate(self, id):
		url = 'https://www.feixiaohao.com/currencies/%s/' % id
		try:
			html = self.getResponse(url).content
			only_a_title = SoupStrainer('div', attrs={'class': 'secondPark'})
			soup = BeautifulSoup(html, "lxml", parse_only=only_a_title)
			values = soup.select('span[class="value"]')
			date = re.findall("\d+",values[3].string)
			if date:
				return '-'.join(date)
			else:
				return ''
		except Exception as e:
			print(e)
			return ''
			
	#上架交易所
	def getNumber(self, id):
		url = 'https://www.feixiaohao.com/currencies/%s/' % id
		try:
			html = self.getResponse(url).content
			only_a_title = SoupStrainer('div', attrs={'class': 'secondPark'})
			soup = BeautifulSoup(html, "lxml", parse_only=only_a_title)
			value = soup.find('a')
			number = re.findall("\d+",value.string)[0]
			return number
		except Exception as e:
			print(e)
			return ''

	#telegram
	def getChat(self, id):
		url = 'https://coinmarketcap.com/currencies/%s/' % id
		try:
			html = self.getResponse(url).content
			only_a_title = SoupStrainer('ul', attrs={'class': 'list-unstyled'})
			soup = BeautifulSoup(html, "lxml", parse_only=only_a_title)
			links = soup.select('span[title="Chat"] ~ a')
			r = []
			for x in links:
				r.append(x['href'])
			return ' , '.join(r)
		except Exception as e:
			print(e)
			return ''
	
	def getLink(self, id):
		url = 'https://coinmarketcap.com/currencies/%s/' % id
		try:
			return url 
		except Exception as e:
			print(e)
			return ''
	
	def dumpCSV(self):
		path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'coin.csv')
		exchangeResult = self.getVolume()
		with open(path, 'w') as f:
			fieldnames = ['rank', 'name', 'link', 'symbol','feixiaohao', 'volume-usd', 'website', 'chat', 'date', 'exchangeNumber']
			wr = csv.DictWriter(f, fieldnames=fieldnames)
			wr.writeheader()
			i = 1
			for x in exchangeResult:
				print(i, x['name'])
				link = self.getLink(x['id'])
				websites = self.getWebSite(x['id'])
				chats = self.getChat(x['id'])
				fei = self.getFeiXiaohaoLink(x['id'])
				date = self.getDate(x['id'])
				number = self.getNumber(x['id'])
				wr.writerow({'rank': x['rank'], 'name': x['name'], 'symbol': x['symbol'], 'link': link, 'feixiaohao': fei, 'volume-usd': x['24h_volume_usd'], 'website': websites, 'chat': chats, 'date': date, 'exchangeNumber': number})
				i += 1

if __name__ == '__main__':
	spider = Spider()
	start = time.time()
	spider.dumpCSV()
	print(time.time() - start)
