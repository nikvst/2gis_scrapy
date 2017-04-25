from enum import Enum
import json

import scrapy


class City(Enum):
    KHV = 35


class ListSpider(scrapy.Spider):

    name = "lists"

    city = City.KHV
    key = 'rutnpt3272'
    start_parent_id = 0
    cookies = {
        '_2gis_webapi_user':
            'a205d8a1-74e5-4333-9575-f353dc7cbe42',
        '_2gis_webapi_session':
            'c568420f-2b0a-49f6-a1f7-9bcf2f20dbe5',
    }
    base_url = 'https://catalog.api.2gis.ru/2.0/catalog/rubric/list'

    def start_requests(self):
        url = '{base_url}?parent_id={parent_id}&region_id={city}&' \
              'sort=popularity&fields=items.rubrics&' \
              'key={key}'.format(base_url=self.base_url,
                                 parent_id=self.start_parent_id,
                                 city=self.city.value,
                                 key=self.key)

        yield scrapy.Request(
            url=url,
            cookies=self.cookies,
            callback=self.parse)

    @staticmethod
    def _print_line_break(file, count):
        for item in range(0, count):
            print('', file=file)

    def parse(self, response):
        filename = '2gis_{}.csv'.format(self.city.name)
        try:
            data = json.loads(response.body_as_unicode())
            data = data['result']
            total = data['total']
            items = data['items']
        except ValueError:
            self.log('Невозможно разобрать json')
            raise
        except KeyError:
            self.log('Некорректная структура json')
            raise

        with open(filename, 'w') as f:
            print('Город: {}. Всего рубрик: {}'.format(
                self.city.name, total), file=f)
            self._print_line_break(f, 2)

            # Вывод рубрик
            print(';Рубрика;branch_count;org_count', file=f)
            for item in items:
                rubric_name = item['name']
                rubric_branch_count = item['branch_count']
                rubric_org_count = item['org_count']

                print(';{};{};{}'.format(
                    rubric_name,
                    rubric_branch_count,
                    rubric_org_count
                ), file=f)

            self._print_line_break(f, 3)

            # Вывод категорий
            print('Рубрика;Категория;branch_count;org_count', file=f)
            for item in items:
                rubric_name = item['name']

                for category in item['rubrics']:
                    category_name = category['name']
                    category_branch_count = category['branch_count']
                    category_org_count = category['org_count']

                    print('{};{};{};{}'.format(
                        rubric_name,
                        category_name,
                        category_branch_count,
                        category_org_count
                    ), file=f)

        self.log('Saved file %s' % filename)
