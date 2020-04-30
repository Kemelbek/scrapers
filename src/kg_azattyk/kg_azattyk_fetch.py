const = 'https://www.azattyk.org'


def fetch_pages(context, data):
    response = context.http.get('https://www.azattyk.org/z/828')
    pages_links = set(response.html.xpath('//div[@class="content"]/a/@href'))
    for link in pages_links:
        if 'live' not in link.split('/')[1]:
            print('LINK: ', const + link)
            data = {'news_link': const+link,
                    'html_link': link.split('/')[-1].split('.')[0]}
            print('HTML LINK: ', link.split('/')[-1].split('.')[0])
            context.emit(data=data)


