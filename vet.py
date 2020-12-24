import scrapy


class VetSpider(scrapy.Spider):
    name = 'vet'
    start_urls = ['http://www.findalocalvet.com/']

    def parse(self, response):
        links = response.css('#SideByCity .itemresult a::attr(href)').getall()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_city)


    def parse_city(self, response):
        links = response.css('.org::attr(href)').getall()
        for link in links:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_clinic)

        next_link = response.css('a.dataheader:contains("Next")::attr(href)').get()
        if next_link:
            next_link = response.urljoin(next_link)
            yield scrapy.Request(next_link, callback=self.parse_city)


    def parse_clinic(self, response):
       yield{
           'Name': response.css('.Results-Header h1::text').get(),
           'City': response.css('.locality::text').get(),
           'State': response.css('.region::text').get(),
           'Phone': response.css('.Phone::text').get(),
           'Link': response.url,
       }

