# -*- coding: utf-8 -*-
import scrapy
import re

class MidiworldClassicSpider(scrapy.Spider):
	name = "midiworldclassic"
	allowed_domains = ["midiworld.com"]
	start_urls = [
		'http://www.midiworld.com/classic.htm/',
	]

	SAVE_PATH = "C://Users/Peng/Documents/GitHub/MusicGenerator/midis/midiworld/classic/" 

	def parse(self, response):

		for url in response.xpath('//a/@href').extract():
			for midiURL in re.findall("http://.+?\.mid$", url):
				yield scrapy.Request(midiURL, callback=self.parseMidiResponse, meta={"composer": "other"})
				pass

		for composerURL in response.xpath("//div[@id='content']/div[@id='page']/div[@align='center']/h5/a/@href").extract():
			yield scrapy.Request("http://www.midiworld.com/" + composerURL, callback=self.handleComposerPage)


	def parseMidiResponse(self, response):
		fileName = response.url.split('/')[-1]
		if len(fileName) < 4 or fileName[-4:] != ".mid":
			return

		composerName = response.request.meta["composer"]

		midiFile = open(self.SAVE_PATH + composerName + "_" + fileName, 'wb')
		midiFile.write(response.body)
		midiFile.close()

	def handleComposerPage(self, response):
		pageName = response.request.url.split('/')[-1]
		composerName = pageName.split(".")[0]

		for url in response.xpath('//a/@href').extract():
			for midiURL in re.findall("http://.+?\.mid$", url):
				yield scrapy.Request(midiURL, callback=self.parseMidiResponse, meta={"composer": composerName})