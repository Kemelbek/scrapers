from datetime import date

today = date.today()


# print(txt)

def fetch_links(context, data):
    response = context.http.get(f'https://kaktus.media?date={today}&lable=8&order=main')
    page = response.html
    links = page.xpath("//div[@class='t f_medium']/a/@href")
    data['links'] = links
    context.emit(data=data)


def fetch_page(context, data):
    links = data['links']
    for link in links:
        response = context.http.get(link)
        data['page'] = response.serialize()
        context.emit(data=data)
