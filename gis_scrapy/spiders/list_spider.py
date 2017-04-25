import scrapy


class ListSpider(scrapy.Spider):
    """
    
    """
    name = "lists"

    def start_requests(self):
        urls = [
            'https://catalog.api.2gis.ru/2.0/catalog/rubric/list?parent_id=0&region_id=35&sort=popularity&fields=items.rubrics&key=rutnpt3272/',
        ]
        for url in urls:
            yield scrapy.Request(
                url=url,
                cookies=[{
                    '_2gis_webapi_user':
                        'a205d8a1-74e5-4333-9575-f353dc7cbe42',
                    '_2gis_webapi_session':
                        'c568420f-2b0a-49f6-a1f7-9bcf2f20dbe5',
                }],
                callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = '123.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
