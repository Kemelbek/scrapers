import re

def extract_data(context, data):
    response = context.http.post('http://www.cadastre.kg/svc-portal/property/searchByAddress.do',
                                 data={'propCode': '1010200110344', 'searchCondition':'ENI', 'searchMode': 'ARS'})
    response1 = context.http.post('http://www.cadastre.kg/svc-portal/property/parcelHistory.do',
                                  data={'id': '01619EF4D435B29C720D897F02E76BED'})
    page = response.html
    page1 = response1.html
    # print( (page.xpath('//dl[@class="mbox1"]/dd/span/text()'))[0])
    old_num = re.findall('[0-9]', page.xpath('//dl[@class="mbox1"]/dd/span/text()')[0])
    new_num = re.findall('[0-9]', page1.xpath('//dd/span/small/strong/text()')[0])
    address = re.sub('\r',' ', page.xpath('//dl[@class="mbox2"]/dd/span/text()')[0].strip())
    article = {'address': address,
               'old number':''.join(old_num),
               'new number':''.join(new_num),
               'url': response.url}


    print(article)

    context.emit(rule='store', data=article)

