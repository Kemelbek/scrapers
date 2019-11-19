import re
import json
import datetime
import locale

def extract_data(context, data):
    response = context.http.get(data['link'])
    page = response.html

    # date = page.xpath('//div/time/text()')[0]
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    str = ''
    str_li = ''
    str_tag = ''

    body = page.xpath('//article/div/p//text()')
    extra_body = page.xpath('//div[ @class ="js-mediator-article"]//li/text()')
    tags_texts = page.xpath('//div[@class="l"]/a/text()')
    tags_urls = page.xpath('//div[@class="l"]/a/@href')

    for el in body:
        str = str + " " + el

    # for el_li in extra_body:
    #     str_li = str_li + " " + el_li
    #
    # for el_tag in tags_texts:
    #     str_tag = str_tag + " " + el_tag

    news = {'news_url': response.url,
            'category': _gettext(page.xpath('//div[@class="janylyk_module_title"]/span/a/text()')),
            'title': _gettext(page.xpath('//h1/text()')),
            'body': _doesexist(str),
            'date': _gettext(page.xpath('//time/@datetime')),
            'author': _gettext(page.xpath('//section/span[2]/text()')),
            'rating': _gettext(page.xpath
                                        ('//span[@id="janylyk_vote"]/text()')),
            'num_of_views_for_last_15_minutes': _gettext(page.xpath('//span[@class="act-stat"]/span[1]/text()'))
            }

    images_scroll = page.xpath('//div[starts-with(@class, "nn-thumb thum-g")]/img/@src')
    images_simple = page.xpath('//div[starts-with(@class, "one-n-img")]/img/@src')
    images_viewer = page.xpath('//p/img/@src')
    print("IMAGES SCROLL : ", images_scroll)
    print("IMAGES SIMPLE : ", images_simple)
    print("IMAGES VIEWER : ", images_viewer)

    images = []
    for image_scroll in images_scroll:
        images.append(image_scroll)
        print("IMAGE SCROLL : ", image_scroll)

    for image_simple in images_simple:
        images.append(image_simple[2:])
        print("IMAGE SIMPLE : ", image_simple)

    for image_viewer in images_viewer:
        images.append('https://www.super.kg'+image_viewer)
        print("IMAGE VIEWER : ", image_viewer)

    image_list = []
    for image in images:
        image_info = {'news_url': response.url,
                      'image_url': image,
                      'file_name': context.http.get(image).content_hash}
        image_list.append(image_info)
        context.emit(rule='download', data={'image_url': image_info['image_url'],
                                            'news_url': image_info['news_url']})

    # tags_list = []
    #
    # for tag, tag_url in zip(tags_texts, tags_urls):
    #     tags_info = {
    #         'news_url': response.url,
    #         'tag_name': tag,
    #         'tag_url': tag_url
    #     }
    #     tags_list.append(tags_info)

    comment_users = page.xpath('//a[@class="user-info"]/text()')
    comment_texts = page.xpath('//div[@class="mess"]/text()')
    comment_dates = page.xpath('//div[@class="date"]/text()')

    comments_list = []



    if len(comment_dates) > 0:
        for comment_user, comment_date in zip(comment_users, comment_dates):
            comments_info = {'news_url': response.url,
                             'comment_author': comment_user.strip(),
                             # 'comment_text': comment_text.strip(),
                             'comment_date': datetime.datetime.strptime(comment_date.strip(), u'%d.%m.%Y. %H:%M')}
            comments_list.append(comments_info)
            print('COMMENTS INFO : ', comments_info)

    comment_text_user =[]
    for comment_text in comment_texts:
        comment_text.strip()
        comment_text_user.append(comment_text)
    print(len(comment_text_user))

    news['images'] = image_list
    news['comments'] = comments_list
    # news['tag_list'] = tags_list

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
