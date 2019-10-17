def extract_data(context, data):
    response = context.http.rehash(data['page'])
    page = response.html

    article = {'title': page.xpath('//h1/text()')[0].strip(),
               'date': page.xpath('//time/text()')[0].strip(),
               'url': response.url}

    print(article)