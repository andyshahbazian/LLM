from pathlib import Path

import scrapy
from scrapy_playwright.page import PageMethod
from scrapy.linkextractors import LinkExtractor

def handler(route):
    return route.abort()

class KBSpider(scrapy.Spider):
    name = "kb"
    output_path = "output/"
    allow_domains = ["docs.aws.amazon.com"]
    urls = [
        "https://docs.aws.amazon.com/index.html"
        ]

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        Path(self.output_path).mkdir(exist_ok=True)
        self.link_extractor = LinkExtractor(allow_domains=self.allow_domains)

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_in_new_context, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                errback=self.errback,
                playwright_page_methods =[
                    PageMethod('wait_for_load_state', state='networkidle', timeout=10000),
                    PageMethod('wait_for_timeout', timeout=3000),
                    PageMethod('route', url='**/*.{png,jpg,jpeg}', handler=handler),
                    PageMethod('route', url='*/**google*/**', handler=handler),
                    PageMethod('route', url='*/**instrument*/**', handler=handler),
                    PageMethod('route', url='*/**network*/**', handler=handler)
                ]
            ))     

    async def parse_in_new_context(self, response): 
        playwright_page = response.meta["playwright_page"]
        await playwright_page.close()

        page = response.url.replace("/","_")
        filename = f"kb-{page}.html"
        Path(self.output_path + filename).write_bytes(response.body)

        for page in self.link_extractor.extract_links(response):
            yield scrapy.Request(url=response.urljoin(page.url), callback=self.parse_in_new_context, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                errback=self.errback,
                playwright_page_methods =[
                    PageMethod('wait_for_load_state', state='networkidle', timeout=10000),
                    PageMethod('wait_for_timeout', timeout=3000),
                    PageMethod('route', url='**/*.{png,jpg,jpeg}', handler=handler),
                    PageMethod('route', url='*/**google*/**', handler=handler),
                    PageMethod('route', url='*/**instrument*/**', handler=handler),
                    PageMethod('route', url='*/**network*/**', handler=handler)
                ]
            ))   

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
