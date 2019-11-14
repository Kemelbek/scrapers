import re
import json
import datetime
import locale
import datetime
import locale



def extract_data(context, data):
    response = context.http.get(data['link'])
    page = response.html

    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    result = datetime.datetime.strptime(page.xpath('//div[@class="col-xs-8 text-right newsDate hidden-xs"]/span[1]/text()'), u'%H:%M, %d %B %Y')
    # article = {'date': f'{result}'}
    # print(article)

    news = {'news_url': response.url,
               'category': _gettext(page.xpath('//div[@class="col-xs-4 newsCat"]/a/text()')),
               'title': _gettext(page.xpath('//a/h1[@class="newsTitle"]/text()')),
               'body': _gettext(result),
               'date': _gettext(page.xpath('//div[@class="col-xs-8 text-right newsDate hidden-xs"]/span[1]/text()')),
               'author': _gettext(page.xpath('//div[@class="col-xs-8 text-right newsDate hidden-xs"]//span[@class="text-nowrap"]/text()')),
             }

    print(news)

    context.emit(rule='store', data=news)





def _gettext(list):
    if not list:
        return '---'
    else:
        return list[0].strip()

