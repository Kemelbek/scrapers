import re
import json
import datetime
import locale


def extract_data(context, data):
    response = context.http.get(data['link'])
    page = response.html

    # print('BODY : ', page.xpath('//div[@class="cont"]/text()')[0])

    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    date = (page.xpath('//div[@class="col-xs-8 text-right newsDate hidden-xs"]/span[1]/text()')[0])
    result = datetime.datetime.strptime(date, u'%H:%M, %d %B %Y')

    str = ''

    body = page.xpath('//div[@class="cont"]/p/text()')

    for el in body:
        str = str + el

    news = {'news_url': response.url,
            'category': _gettext(page.xpath('//div[@class="col-xs-4 newsCat"]/a/text()')),
            'title': _gettext(page.xpath('//a/h1[@class="newsTitle"]/text()')),
            'body': _doesexist(str),
            'date': _doesexist(result),
            'author': _gettext(page.xpath(
                '//div[@class="col-xs-8 text-right newsDate hidden-xs"]//span[@class="text-nowrap"]/text()')),
            }

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
