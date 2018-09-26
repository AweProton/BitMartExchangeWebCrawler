# coding: utf-8
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import csv
import os
import time
import lxml

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

	def getCoinList(self):
		url = 'https://files.coinmarketcap.com/generated/search/quick_search.json'
		try:
			resp = self.getResponse(url)
		except Exception as e:
			print(e)
		return resp.json()
		
	def getVolume(self):
		url = 'https://api.coinmarketcap.com/v1/ticker/?limit=2000'
		try:
			resp = self.getResponse(url)
		except Exception as e:
			print(e)
		return resp.json()

	def getWebSite(self, slug):
		url = 'https://coinmarketcap.com/currencies/%s/' % slug
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
	
	def getChat(self, slug):
			url = 'https://coinmarketcap.com/currencies/%s/' % slug
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
	
	def getLink(self, slug):
				url = 'https://coinmarketcap.com/currencies/%s/' % slug
				try:
					return url 
				except Exception as e:
					print(e)
					return ''
	
	def dumpCSV(self):
		path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'coin.csv')
		results = self.getCoinList()
		exchangeResult = self.getVolume()
		with open(path, 'w') as f:
			fieldnames = ['rank', 'name', 'link', 'symbol', 'volume', 'website', 'chat']
			wr = csv.DictWriter(f, fieldnames=fieldnames)
			wr.writeheader()
			i = 1
			for x, y in zip(results, exchangeResult):
				print(i, x['name'])
				link = self.getLink(x['slug'])
				websites = self.getWebSite(x['slug'])
				chats = self.getChat(x['slug'])
				wr.writerow({'rank': x['rank'], 'name': x['name'], 'symbol': x['symbol'], 'link': link, 'volume': y['24h_volume_usd'], 'website': websites, 'chat': chats})
				i += 1

if __name__ == '__main__':
	spider = Spider()
	start = time.time()
	spider.dumpCSV()
	print(time.time() - start)