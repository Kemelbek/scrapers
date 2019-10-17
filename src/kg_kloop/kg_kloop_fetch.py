def fetch_links(context, data):
    response = context.http.get('https://kloop.kg/news/')
    page = response.html
    links = page.xpath('//h3/a/@href')
    data['links'] = links
    context.emit(data=data)


def fetch_page(context, data):
    links = data['links']
    for link in links:
        response = context.http.get(link)
        data['page'] = response.serialize()
        context.emit(data=data)
