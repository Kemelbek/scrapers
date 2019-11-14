const = 'https://24.kg'
def fetch_pages(context, data):
    response = context.http.get('https://24.kg')
    pages_links = set(response.html.xpath('//div/div[@class="title"]/a/@href'))
    for link in pages_links:
        print('LINK: ', const + link)
        data['link'] = const + link
        context.emit(data=data)

