import re
import json
import datetime
import locale

def extract_data(context, data):
    response = context.http.get(data['link'])
    page = response.html

    secur_el = _doesexist(page.xpath('//tr[10]/td[2]/text()'))
    emis_el = _doesexist(page.xpath('//tr[11]/td[2]/text()'))

    check_security = _checktype(secur_el[0])
    check_emission = _checktype(emis_el[0])

    first_emission_placement_price = ''.join(''.join(re.findall(r'\d+[\W+\d]', check_emission[0])).split())
    first_emission_placement_currency = (re.findall('сом', check_emission[0]))

    second_emission_placement_price = ''.join(''.join(re.findall(r'\d+[\W+\d]', check_emission[1])).split())
    second_emission_placement_currency = (re.findall('сом', check_emission[1]))

    normal_securities_num = ''.join(''.join(re.findall(r'\d+[\W+\d]', check_security[0])).split())
    normal_securities_unit = (re.findall('шт', check_security[0]))

    privileged_securities_num = ''.join(''.join(re.findall(r'\d+[\W+\d]', check_security[1])).split())
    privileged_securities_unit = (re.findall('шт', check_security[1]))

    company = {'company_url': response.url,
               'company_name': _gettext(page.xpath('//tr[2]/td[2]/text()')),
               'occupation_type': _gettext(page.xpath('//tr[3]/td[2]/text()')),
               'name_surname_of_supervisor': _gettext(page.xpath('//tr[4]/td[2]/text()')),
               'supervisors_position': _gettext(page.xpath('//tr[5]/td[2]/text()')),
               'address': _gettext(page.xpath('//tr[6]/td[2]/text()')),
               'phone_number_fax': _gettext(page.xpath('//tr[7]/td[2]/text()')),
               'registrar': _gettext(page.xpath('//tr[8]/td[2]/text()')),
               'securities_type': _gettext(page.xpath('//tr[9]/td[2]/text()')),
               'quantity_of_securities': _gettext(page.xpath('//tr[10]/td[2]/text()')),
               'normal_securities_quantity': _doesexist(normal_securities_num),
               'normal_securities_unit': _gettext(normal_securities_unit),
               'privileged_securities_num': _doesexist(privileged_securities_num),
               'privileged_securities_unit': _gettext(privileged_securities_unit),
               'first_emission_placement_price': _doesexist(first_emission_placement_price),
               'first_emission_placement_currency': _gettext(first_emission_placement_currency),
               'second_emission_placement_price': _doesexist(second_emission_placement_price),
               'second_emission_placement_currency': _gettext(second_emission_placement_currency)
               }
    # reports = {'company_url': response.url,
    #            'quarterly_report_url': _gettext(page.xpath('//tr[1]/td[2]/a/@href')),
    #            'annual_report_url': _gettext(page.xpath('//tr[2]/td[2]/a/@href'))}

    reports = page.xpath('//tr/td[2]/a/@href')
    report_list = []
    for report in reports:
        report_info = {'report_url': report,
                       'company_url': response.url,
                       'file_name': context.http.get(report).content_hash}

        report_list.append(report_info)
        context.emit(rule='download', data={'report_url': report_info['report_url'],
                                            'company_url': report_info['company_url']})
    #
    # context.emit(rule='download', data=report_list)
    #

    # if reports['quarterly_report_url'] or reports['annual_report_url']:
    #     context.emit(rule='download', data={'quarterly_report_url': reports['quarterly_report_url'],
    #                                         'annual_report_url': reports['annual_report_url'],
    #                                         'company_url': reports['company_url']})

    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    news_date = page.xpath('//td/strong/text()')
    news_urls = page.xpath('//a[contains(@href,"Russ")]/@href')
    news_titles = page.xpath('//a[contains(@href,"Russ")]/text()')
    res = []
    for date, news_url, news_title in zip(news_date, news_urls, news_titles):
        news_info = {'company_url': response.url,
                     'title': news_title,
                     'date': datetime.datetime.strptime(date, u'%d.%m.%Y'),
                     'news_url': news_url}
        res.append(news_info)

    company['news_info'] = res
    company['reports'] = report_list

    print(company)
    context.emit(rule='store', data=company)


def _doesexist(string):
    if not string:
        return '---'
    else:
        return string


def _gettext(list):
    if not list:
        return '---'
    else:
        return list[0].strip()


def _checktype(list):
    if ';' in list:
        return list.split(';')

    else:
        return [list, 'none']
