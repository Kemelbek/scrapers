import re
import json
import datetime
import locale

def extract_data(context, data):
    # response = context.http.rehash(data['page'])
    response = context.http.get(data['link'])
    page = response.html

    date = page.xpath('//time/text()')[0]
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    str = ''
    str_li = ''
    str_tag = ''

    body = page.xpath('//div[@class="js-mediator-article"]//p/text()')
    extra_body = page.xpath('//div[ @class ="js-mediator-article"]//li/text()')
    tags_texts = page.xpath('//div[@class="l"]/a/text()')
    tags_urls = page.xpath('//div[@class="l"]/a/@href')

    for el in body:
        str = str + " " + el

    for el_li in extra_body:
        str_li = str_li + " " + el_li

    for el_tag in tags_texts:
        str_tag = str_tag + " " + el_tag

    news = {'news_url': response.url,
            'title': _gettext(page.xpath('//h1/text()')),
            'body': _doesexist(str),
            'extra_body': _doesexist(str_li),
            'date': datetime.datetime.strptime(date, u'%d %B %Y %H:%M'),
            'number_of_views': _gettext(page.xpath
                                        ('//div[@class="topic_view_and_message"]//span[contains(text(), " ")]/text()')),
            'tags': _doesexist(str_tag)
            }

    images_scroll = page.xpath('//div[@class="topic-gallery-none"]/img/@src')
    # images_simple = page.xpath('//img[@style="display:none;"]/@src')
    images_viewer = page.xpath('//a[@style="display: block;"]//@src')
    # print("IMAGES SIMPLE : ", images_simple)
    print("IMAGES VIEWER : ", images_viewer)

    images = []
    for image_scroll in images_scroll:
        images.append(image_scroll)
        print("IMAGES SCROLL : ", image_scroll)

    # for image_simple in images_simple:
    #     images.append(image_simple)
    #     print("IMAGES SIMPLE : ", image_simple)

    for image_viewer in images_viewer:
        images.append(image_viewer)
        print("IMAGES VIEWER : ", image_viewer)

    image_list = []
    for image in images:
        image_info = {'news_url': response.url,
                      'image_url': image,
                      'file_name': context.http.get(image).content_hash}
        image_list.append(image_info)
        context.emit(rule='download', data={'image_url': image_info['image_url'],
                                            'news_url': image_info['news_url']})

    tags_list = []

    for tag, tag_url in zip(tags_texts, tags_urls):
        tags_info = {
            'news_url': response.url,
            'tag_name': tag,
            'tag_url': tag_url
        }
        tags_list.append(tags_info)

    comment_users = page.xpath('//div[following-sibling::div[@class="date"]]|a//text()')
    comment_dates = page.xpath('//div[@class="date"]//text()')

    comments_list = []
    index = 1

    if len(comment_dates) > 0:
        for comment_user,  comment_date in zip(comment_users,  comment_dates):

            comments_info = {'news_url': response.url,
                             'comment_author': comment_user.strip(),
                             'comment_text': page.xpath
                             (f'//div[@class="message j_message "][{index}]/div[@class="clearfix"]/div[@class="text"]//text()'),
                             'comment_date': datetime.datetime.strptime(comment_date, u'%d.%m.%Y %H:%M')}
            comments_list.append(comments_info)
            index = index + 1
            print('COMMENTS INFO : ', comments_info)

    news['images'] = image_list
    news['comments'] = comments_list
    news['tag_list'] = tags_list

    print("NEWS: ", news)

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
