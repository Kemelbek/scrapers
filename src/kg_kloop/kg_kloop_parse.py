# timeData = '24 октября 17 07:24'

import datetime
import locale


def extract_data(context, data):
    response = context.http.rehash(data['page'])
    page = response.html
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    timeDate = page.xpath('//time/text()')[0].strip()
    result = datetime.datetime.strptime(timeDate,
                                        u'%d %B %Y')

    article = {'title': page.xpath('//h1/text()')[0].strip(),
               'author': page.xpath('//div[@class="td-post-author-name"]/a/text()')[0].strip(),
               'date': f'{result}',
               'url': response.url}

    print(article)

    context.emit(rule='store', data=article)