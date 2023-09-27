import scrapy
from junior_offers.items import JobOfferItem

class NofluffjobsspiderSpider(scrapy.Spider):
    name = "nofluffjobsspider"
    allowed_domains = ["nofluffjobs.com"]
    start_urls = ["https://nofluffjobs.com/pl/?criteria=employment%3Dzlecenie%20seniority%3Dexpert&page=1"]

    def parse(self, response):
        offers = response.css("div.list-container")[0].css("a.posting-list-item::attr(href)").getall()
        print(f"\n\n{offers}\n\n")
        for offer in offers:
            offer_page_url = "https://nofluffjobs.com" + offer
            yield response.follow(offer_page_url, callback=self.offer_page_parse)

        next_page = response.xpath('//a[@aria-label="Next"]').xpath("@href").get(default=None)
        if next_page is not None:
            next_page_url =  "https://nofluffjobs.com" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    def offer_page_parse(self,response):
        salariesInfo = {
            'salaries': response.css(".salary h4::text").getall(),
            'salariesTypes': response.css(".salary div span::text").getall(),
        }

        locations = response.css(".locations-compact li div::text").get(default=None)
        if locations is not None:
            locations = response.css(".locations div.popover-body div ul li a span::text").getall()
            if len(locations) == 0:
                locations = response.css(".popover-locations div.popover-body ul li a::text").getall()
            locations.append(response.css("common-posting-locations.locations div span span::text").get(default=""))
        
        companyUrl = response.xpath("//a[@id='postingCompanyUrl']").xpath("@href").get(default=None)
        if companyUrl is not None:
            companyUrl = "https://nofluffjobs.com" + companyUrl

        jobItem = JobOfferItem()
        jobItem['company'] = response.css("div.posting-details-description a::text").get()
        jobItem['position'] = response.css("div.posting-details-description h1::text").get()
        jobItem['salary'] = salariesInfo
        jobItem['locations'] = locations
        jobItem['logoUrl'] = response.xpath("//img[@alt='job offer company pixel logo']").attrib["src"]
        jobItem['offerUrl'] = response.url
        jobItem['companyUrl']=  companyUrl
        jobItem['stack' ]= response.xpath("//div[@id='posting-requirements']/section/ul/li/span/text()").getall()
        yield jobItem