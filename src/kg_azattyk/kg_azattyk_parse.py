import re
import json
import datetime
import locale

const = 'https://www.azattyk.org/'


def extract_data(context, data):
    response = context.http.get(data['news_link'])
    response_comments = context.http.get(const+'comments/a'+data['html_link']+'p1000s0sa0.html')

    page = response.html
    page_comments = response_comments.html
    str = ''

    body = page.xpath('//div[@class="wsw"][parent::div[@id="article-content"]]/p/text()')

    for el in body:
        str = str + el

    news = {'news_url': response.url,
            'category': _gettext(page.xpath('//div[@class="category"]/a/text()')),
            'title': _gettext(page.xpath('//h1/text()')),
            'body': _doesexist(str),
            'date': _gettext(page.xpath('//time/@datetime')),
            'author': _gettext(page.xpath(
                '//a[@class="links__item-link"]/text()')),
            }

    images = page.xpath('//figure/div[@class="img-wrap"]//img/@src')
    image_list = []
    for image in images:
        image_info = {'news_url': response.url,
                      'image_url': image,
                      'file_name': context.http.get(image).content_hash}
        image_list.append(image_info)
        context.emit(rule='download', data={'image_url': image_info['image_url'],
                                            'news_url': image_info['news_url']})

    comment_users = page_comments.xpath('//span[@class="user"]/text()')
    comment_texts = page_comments.xpath('//div[@class="comment__content"]/p/text()')
    comment_dates = page_comments.xpath('//span[@class="date"][preceding-sibling::span]/text()')

    comments_list = []

    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    for comment_user, comment_text, comment_date in zip(comment_users, comment_texts, comment_dates):
        comments_info = {'news_url': response.url,
                         'comment_author': comment_user.strip(),
                         'comment_text': comment_text.strip(),
                         'comment_date': datetime.datetime.strptime(comment_date, u'%d,%m,%Y %H:%M')}
        comments_list.append(comments_info)
        print('COMMENTS INFO : ', comments_info)

    news['images'] = image_list
    news['comments'] = comments_list

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
