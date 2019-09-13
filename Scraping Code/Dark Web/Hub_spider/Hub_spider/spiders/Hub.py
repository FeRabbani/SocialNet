# -*- coding: utf-8 -*-
#Scrapy code for crawling data from .onion sites 
#requirement: scrapy package
# Here we extract all threads title and url in first function and then by using second one, all posts and data inside each thread



import time
import scrapy
import requests as r
from scrapy import Request

class HubSpider(scrapy.Spider):
    name = 'Hub'
   
    start_urls = ['http://phoenixvso7f5ypt.onion/archives/HUB%20ARCHIVE/thehub7gqe43miyc.onion.link/index_bebf4d5a.php.html']   #URL

    def parse(self, response):
        
   
        all_threads=response.xpath('//td/div/strong/span  | //td/div/span')       
        
        
        for thread in all_threads:
            relative_url = thread.xpath('a/@href').extract_first()      
            title = thread.xpath('a/text()').extract_first()
            absolute_url = 'http://phoenixvso7f5ypt.onion/archives/HUB ARCHIVE/thehub7gqe43miyc.onion.link'+relative_url[1:]   #extract url for each thread 
            yield Request(absolute_url, callback=self.parse_page, meta={'URL':absolute_url})
        
        Navigate=response.xpath('//div[@class="pagelinks floatleft"]/text()[normalize-space(.)= "]"]/following-sibling::a[1]')  #Navigate on pages
        relative_next=Navigate.xpath('@href').extract_first()
 
       
        if relative_next:
           absolute_next_url='http://phoenixvso7f5ypt.onion/archives/HUB%20ARCHIVE/thehub7gqe43miyc.onion.link'+ relative_next[1:]
           yield Request (absolute_next_url, callback=self.parse)
       
        
    def parse_page(self, response):       #function for extracting data 

        Thread=[]
        Comment=[]
        Date_list=[]requirment
        url = response.meta.get('URL')
        P_title =response.xpath('//li[@class="last"]/a/span/text()').extract_first()
        Dates=response.xpath('string(.//div[@class="smalltext"])').extract()
        
            
        posts =response.xpath('//div[@class="post"]')
       
        for post in posts:
            
            
            Message=post.xpath('string(.//div[@class="inner"])').extract()

            Comment.append(Message)
            Thread.append(P_title)
            #yield{'POst':Message} 
             

        
        Membername= response.xpath('//div[@class="poster"]/h4/a/text()').extract()
        #yield{'thread': P_title,'Memner:':Membername} 
        for item in zip(Membername,Thread,Comment,Dates):
            #create a dictionary to store the scraped info
            scraped_info = {
                'Member' : item[0],
                'Thread': item[1],
                'Message': item[2],
                'Date' : item[3],
            }

          
            yield scraped_info
             
        page_index=response.xpath('//div[@class="pagelinks floatleft"]/text()[normalize-space(.)= "]"]/following-sibling::a[1]') #for number of pages in each thraed
        link=page_index.xpath('@href').extract_first()
        if link:
           
           absolute_next_url='http://phoenixvso7f5ypt.onion/archives/HUB ARCHIVE/thehub7gqe43miyc.onion.link'+ link[1:]
           yield Request (absolute_next_url, callback=self.parse_page)
        
    

   
   


