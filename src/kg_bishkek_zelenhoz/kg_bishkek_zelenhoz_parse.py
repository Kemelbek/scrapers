BASE_URL = 'https://www.facebook.com'

def extract_data(context, data):
    response = context.http.get('https://www.facebook.com/pg/mpbishzelenhoz/posts/')
    # response1 = context.http.rehash(response.serialize())
    page = response.html
    dates = page.xpath('//div/span/span/a/abbr/@title')
    headers = page.xpath('//div/div[@data-testid="post_message"]//p//text()')
    urls = page.xpath('//span/span[@class="fsm fwn fcg"]/a/@href')
    res = []
    for url in urls:
        article = {
                    # 'date': _doesexist(date),
                   # 'header': header,
                   'url': _doesexist(BASE_URL+url)}
        print(article)
        context.emit(rule='store', data=article)


def _gettext(list):
    if not list:
        return '---'
    else:
        return list[0].strip()


def _doesexist(string):
    if not string:
        return '---'
    else:
        return string