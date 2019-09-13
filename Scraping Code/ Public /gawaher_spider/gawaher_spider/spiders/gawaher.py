# -*- coding: utf-8 -*-
#In this script we use scrapy packages for crawling data in public pages 



import scrapy
from scrapy import Request

class GawaherSpider(scrapy.Spider):
    name = 'gawaher'
   
    start_urls = ['https://www.gawaher.com/']

    
    
    def parse(self, response):          # this function has been used for Extracting all thrads and URL in forums
        
        all_threads= response.xpath('//span[@class="ipsType_break ipsContained"]')
 
        for thread in all_threads:
            relative_url = thread.xpath('a/@href').extract_first()      # extracting URL for each thread in forums 
            if relative_url!=None : 
               absolute_url = response.urljoin(relative_url)
               title = thread.xpath('span/text()').extract_first()
               yield Request(absolute_url, callback=self.parse_page, meta={'URL':absolute_url,'Title': title})
         
        

        
        relative_next_url=response.xpath('//li[@class="ipsPagination_next"]/a[@rel="next"]/@href').extract_first()
        

        if relative_next_url:
           absolute_next_url=relative_next_url
           yield Request (absolute_next_url, callback=self.parse)

    def parse_page(self, response):       # this function has been used for crawling data in each thread such as membername,posts,date,threadname,...

        Thread=[]
        MESSAGE=[]
        Re_ID=[]
        url = response.meta.get('URL')
        P_title =response.xpath('//div/h1/span[@class="ipsType_break ipsContained"]/span/text()')[-1].extract()
        Dates=response.xpath('//a/time/text()').extract()
            
        posts =response.xpath('//div[@class="cPost_contentWrap ipsPad"]')
       
        for post in posts:   
            
            
            Message=post.xpath('string(.//div[@data-role="commentContent"])').extract()
            REPLY_ID=post.xpath('div/blockquote/@data-ipsquote-contentcommentid').extract()
            MESSAGE.append(Message)
            Thread.append(P_title)
            if not REPLY_ID:
               REPLY_ID=str(0)
               Re_ID.append(REPLY_ID)
            else:
               Re_ID.append(REPLY_ID)
             

      
        Membername= response.xpath('//aside/h3/strong/a/text()').extract()    
        POST_ID= response.xpath('//div[@class="ipsColumn ipsColumn_fluid"]/div/@data-commentid').extract()   

        for item in zip(Membername,Thread,MESSAGE,Dates,POST_ID,Re_ID):
            #create a dictionary to store the scraped info
            scraped_info = {
                'Member' : item[0],
                'Thread': item[1],
                'Message': item[2],
                'Date' : item[3],
                'Post-Id' : item[4],
                'Reply-Id' : item[5],
            }

          
            yield scraped_info
             
        relative_next=response.xpath('//li[@class="ipsPagination_next"]/a[@rel="next"]/@href').extract_first()  #Navigate on pages 
        
        if relative_next:
           absolute_next =relative_next
            
           yield Request(absolute_next, callback=self.parse_page)
        

   
  

  
