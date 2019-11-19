from datetime import date

today = date.today()


def fetch_links(context, data):
    response = context.http.get('https://www.super.kg/kabar/')
    links = set(response.html.xpath
                ("//div[@class='news_text']/a[@class='kabarlink']/@href|//div[@class='clear'][10]/a/@href"))
    for link in links:
        data['link'] = 'https://www.super.kg' + link
        context.emit(data=data)


