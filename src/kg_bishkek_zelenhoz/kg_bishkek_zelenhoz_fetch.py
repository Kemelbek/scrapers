# def fetch_pages_links(context, data):
#     response = context.http.get('https://www.facebook.com/pg/mpbishzelenhoz/posts')
#     pages_links = set(response.html.xpath('//div/a[contains(@href, "Page")]/@href'))
#     for link in pages_links:
#         print('LINK: ', link)
#         data['page_link'] = link
#         context.emit(data=data)
#
#
# def fetch_page_link(context, data):
#     page_link = data['page_link']
#     response = context.http.get(page_link)
#     companies_links = response.html.xpath('//td/a/@href')
#     for link in companies_links:
#         data['link'] = link
#         context.emit(data=data)
