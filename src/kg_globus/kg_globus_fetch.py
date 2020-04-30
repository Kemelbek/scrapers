const = 'https://globus-online.kg'


def fetch_pages(context, data):
    response = context.http.get('https://globus-online.kg/catalog/napitki/soki_naturalnye/')
    pages_links = set(response.html.xpath('//div[@class="navigation"]/a/@href'))
    for link in pages_links:
        print('LINK: ', const + link)
        data['link'] = const + link
        context.emit(data=data)

