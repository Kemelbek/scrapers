import re
import json
import datetime
import locale

const = 'https://24.kg'


def extract_data(context, data):
    response = context.http.get(data['link'])
    page = response.html

    seen_full = page.xpath('//div[@class="col-xs-12 col-sm-8 newsLink"]/text()[preceding-sibling::br]')[0]

    y = re.findall('[0-9]', seen_full)
    seen = ''.join(y)


    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    date = (page.xpath('//div[@class="col-xs-8 text-right newsDate hidden-xs"]/span[1]/text()')[0])
    result = datetime.datetime.strptime(date, u'%H:%M, %d %B %Y')

    body_str = ''

    body = page.xpath('//div[@class="cont"]/p//text()')

    for el in body:
        body_str = body_str +" "+ el

    print('BODY : ', body_str)

    news = {'news_url': response.url,
            'category': _gettext(page.xpath('//div[@class="col-xs-4 newsCat"]/a/text()')),
            'title': _gettext(page.xpath('//a/h1[@class="newsTitle"]/text()')),
            'body': _doesexist(body_str),
            'date': _doesexist(result),
            'author': _gettext(page.xpath(
                '//div[@class="col-xs-8 text-right newsDate hidden-xs"]//span[@class="text-nowrap"]/text()')),
            'number_of_views': _doesexist(seen)
            }

    print(news)

    images = page.xpath('//div[@class="cont"]//a/@href')
    image_list = []
    for image in images:
        if 'files' in image:
            image_url = const+image
            image_info = {'news_url': response.url,
                          'image_url': image_url,
                          'file_name': context.http.get(image_url).content_hash}
            image_list.append(image_info)
            context.emit(rule='download', data={'image_url': image_info['image_url'],
                                                'news_url': image_info['news_url']})

    news['images'] = image_list

    print(news)

    context.emit(rule='store', data=news)


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
