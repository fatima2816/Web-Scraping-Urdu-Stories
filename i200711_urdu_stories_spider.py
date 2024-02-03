#Fatima Abdul Wahid 
#20i-0711
#i200711@nu.edu.pk

import scrapy
import re
import csv

class I200711UrduStoriesSpider(scrapy.Spider):
    name = 'urdu_story'
    start_urls = ['https://www.urduzone.net/']
    count=2
    max=226
    url2='https://www.urduzone.net/page/2/?s=+'
    current_page=2

  
    def parse(self, response):
           
           #navigate from search bar by searching space bar 
            yield scrapy.FormRequest.from_response(
            response,
            formid={'td-header-search':' '},  
            
            callback=self.parse_next_page
        )

           
        

    def parse_next_page(self,response):
      
           
         link_container = response.css('div.item-details')
       
         for next in link_container.css('a::attr(href)').getall():
             yield response.follow(next, callback=self.parse_link)
        
        

        #move to the page 2 of stories
         yield response.follow(self.url2, callback=self.parse_next_page2)
      


    def parse_next_page2(self,response):
      
        link_container = response.css('div.item-details')
       
        for next in link_container.css('a::attr(href)').getall():
            yield response.follow(next, callback=self.parse_link)

        #iterate over all pages till 226 starting from the second page to print stories
        while self.count < self.max:
           
           self.count+=1
           # Increment the current page number
           self.current_page += 1  
           
            # Build the URL for the next page
           next_page_url = f'https://www.urduzone.net/page/{self.current_page}/?s=+'
           yield response.follow(next_page_url, callback=self.parse_next_page3)
        

    def parse_next_page3(self,response):
        

        link_container = response.css('div.item-details')
       
        for next in link_container.css('a::attr(href)').getall():
            yield response.follow(next, callback=self.parse_link)
            
   
        
    def parse_link(self, response):
      
         

        # Extract all lines of text from the page
        stories = response.css('*::text').getall()

        # Define a regular expression
        urdu_pattern = r'[آ-ے،۔]+'

        # Create an empty string to store the concatenated Urdu words
        urdu_string = ''

        # Iterate through each line and extract Urdu words
        for line in stories:
            #remove this line which is not a part of any story
            if "تین عورتیں تین کہانیاں" in line:
                line = line.replace("تین عورتیں تین کہانیاں", "")

            urdu_words = re.findall(urdu_pattern, line)

            # Concatenate the Urdu words into a single string
            urdu_string += ' '.join(urdu_words) + ' '

        #leave two lines after end of each story 
        urdu_string += '\n\n'   
        # Append the concatenated Urdu word string to the CSV file
        with open('i200711_urdu_stories.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['urdu_words']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the concatenated Urdu word string to the CSV file
            writer.writerow({'urdu_words': urdu_string.strip()})

       #yield for printing output
        # yield {
        #     'urdu_words': urdu_string.strip()
        # }
       
            
