import re
import json
import datetime
import locale

const = 'https://24.kg'


def extract_data(context, data):
    response = context.http.get(data['link'])
    page = response.html

    goods = {'page_url': response.url,
            'name': _gettext(page.xpath('//div[@class="list-showcase__name"]//text()')),
            'price': _gettext(page.xpath('//span[@class="c-prices__value js-prices_pdv_ГЛОБУС Розничная"]/text()')) + " сом/шт",
            }

    print(goods)

    # images = page.xpath('//div[@class="cont"]//a/@href')
    # image_list = []
    # for image in images:
    #     if 'files' in image:
    #         image_url = const+image
    #         image_info = {'news_url': response.url,
    #                       'image_url': image_url,
    #                       'file_name': context.http.get(image_url).content_hash}
    #         image_list.append(image_info)
    #         context.emit(rule='download', data={'image_url': image_info['image_url'],
    #                                             'news_url': image_info['news_url']})

    # news['images'] = image_list

    print(goods)

    context.emit(rule='store', data=goods)


def _gettext(list):
    if not list:
        return '---'
    else:
        return list[0].strip()


def _doesexist(str):
    if not str:
        return '---'
    else:
        return str
