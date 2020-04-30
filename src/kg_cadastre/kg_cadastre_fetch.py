# def fetch_links(context, data):
#     response = context.http.post('http://www.cadastre.kg/svc-portal/app/civilPage.do', data={'1-01-02-0011-0311-01-004'})
#     page = response.html
#     links = page.xpath('//dd/span/text()')
#     data['links'] = links
#     context.emit(data=data)
#
#
# def fetch_page(context, data):
#     links = data['links']
#     for link in links:
#         response = context.http.get(link)
#         data['page'] = response.serialize()
#         context.emit(data=data)

