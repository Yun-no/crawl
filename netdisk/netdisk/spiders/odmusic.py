# -*- coding: utf-8 -*-
import scrapy
import os


class OdmusicSpider(scrapy.Spider):
    name = 'odmusic'
    allowed_domains = ['od.lezi.me']
    start_urls = ['https://od.lezi.me/music/%E5%91%A8%E6%9D%B0%E4%BC%A6%E5%85%A8%E9%83%A8%E4%B8%93%E8%BE%91-%E6%97%A0%E6%8D%9F%E9%9F%B3%E8%B4%A8%E7%89%88/']

    def parse(self, response):
        for folder in response.xpath('//li[@data-sort-name]/a[not(@class)]'):
            folderlink = folder.xpath("./@href").extract_first()
            foldername = folder.xpath("./div/span/text()").extract_first()
            yield scrapy.Request(url=response.urljoin(folderlink), callback=self.parsefolder, meta={'foldername': foldername})

    def parsefolder(self, response):
        foldername = response.meta['foldername']
        folderpath = 'D:/music/zjl/' + foldername
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)
        for musictag in response.xpath("//li[contains(@class, 'file')]/a[@class='audio']"):
            musiclink = musictag.xpath("./@href").extract_first()
            musicname = folderpath + '/' +musictag.xpath("./@data-name").extract_first()
            #yield {musicname: musiclink}
            if os.path.isfile(musicname):
                pass
            else:
                yield scrapy.Request(url=response.urljoin(musiclink), callback=self.downloadmusic, meta={'filename': musicname})
        for folder in response.xpath('//li[@data-sort-name]/a[not(@class)]'):
            folderlink = folder.xpath("./@href").extract_first()
            foldername = folder.xpath("./div/span/text()").extract_first()
            yield scrapy.Request(url=response.urljoin(folderlink), callback=self.parsefolder, meta={'foldername': foldername})

    def downloadmusic(self, response):
        path = response.meta['filename']
        if os.path.isfile(path):
            pass
        else:
            with open(path, 'wb') as f:
                f.write(response.body)

