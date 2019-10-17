timeData = '08 октября 17'

import re
import datetime
import locale
    #
    # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    # result = datetime.datetime.strptime(timeData, u'%d %B %y')
    # article = {'date': f'{result}'}
    # print(article)
    #
    #
    #
    # locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    # timeDate = '12.05.2014'
    # result_date = datetime.datetime.strptime(timeDate,
    #                                          u'%d.%m.%Y')

def _checktype(list):
    if ';' in list:
        return list.split(';')
    else:
        return [list, '']

# z = ['простые - 373 473 шт.; привилегированные - 8 164 шт.']
z = ['500 335 шт.']
# z = ['2 747 242 шт.']
x = _checktype(z[0])
re.findall('[а-яА-Я]', z[0])
y = re.findall('[0-9]', z[0])
res = ''.join(re.findall('[а-яА-Я]', z[0])).split()

check_security = _checktype(z[0])
normal_securities_num = ''.join(''.join(re.findall(r'\d+[\W+\d]', check_security[0])).split())
normal_securities_unit = (re.findall('шт', check_security[0]))
# first_emission_placement_currency = (re.findall('сом', x[0]))

second_emission_placement_price = ''.join(''.join(re.findall(r'\d+[\W+\d]', x[1])).split())
second_emission_placement_currency = (re.findall('сом', x[1]))


# normal_securities_type = (re.findall('простые', x[0]))
# normal_securities_num = ''.join(''.join(re.findall(r'\d+[\W+\d]', x[0])).split())

normal_securities_unit = (re.findall('шт', x[0]))


# priviliged_securities_type = (re.findall('привилегированные', x[1]))
priviliged_securities_num = ''.join(re.findall('[\d+\W]', x[1])).split()
priviliged_securities_unit = (re.findall('шт', x[1]))

foo = ';' in z[0]
u = [z[0]]

print(normal_securities_num, normal_securities_unit)

# print(normal_securities_num, first_emission_placement_price, second_emission_placement_price, second_emission_placement_currency)
#
# import json
# import facebook
#
# def main():
#     token ={}
#
#     graph = facebook.GraphAPI(token)
#
#     fields = ['id', 'name', 'about']
#
#     fields = ''.join(fields)
#
#     page = graph.get_object("mpbishzelenhoz", fields=fields)
#
#     print(json.dumps(page, indent=4))
#
# if __name__ == "__main___":
#     main()