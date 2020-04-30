from kg_act_sot.date_converter import Converter as converter
import kg_act_sot.constants as const


def extract(context, data):
    page = context.http.rehash(data['case_page'])
    case_data = {
        'case_url': data['case_url'],
        'case_name': get_data(page, 'Наименование дела'),
        'case_number': get_data(page, 'Номер дела'),
        'case_type': get_data(page, 'Тип дела'),
        'case_condition': get_data(page, 'Состояние дела'),
        'case_status': get_data(page, 'Статус дела'),
        'plaintiff': get_data(page, 'Истец'),
        'defendant': get_data(page, 'Ответчик'),
        'site_reg_date': converter.convert(get_data(page, 'Регистрация на сайте')),
        'judge': get_data(page, 'Судья докладчик'),
        'court': get_data(page, 'Суд'),
        'court_address': get_data(page, 'Адрес суда'),
        'court_contact_info': get_data(page, 'Контакты суда'),
        'act_file_url': get_act_file_url(page)

    }
    acts = []
    meetings = []
    index = 1
    for meeting in range(len(page.html.xpath("//div[@id='meetings']//tbody/tr"))):
        meeting = {
            'url': data['case_url'],
            'meeting_date': converter.convert(get_meeting_info(page, index, 1)),
            'court': get_meeting_info(page, index, 2),
            'judge': get_meeting_info(page, index, 3),
            'pub_on_site': converter.convert(get_meeting_info(page, index, 4)),
        }
        index += 1
        meetings.append(meeting)

    index = 1
    for act in range(len(page.html.xpath("//div[@id='acts']//tbody/tr"))):
        act = {
            'url': data['case_url'],
            'act_name': get_act_info(page, index, 1),
            'act_download_url': get_act_download_url(page),
            'act_type': get_act_info(page, index, 2),
            'act_date': converter.convert_date(get_act_info(page, index, 3)),
            'pub_on_site': converter.convert(get_act_info(page, index, 4))
        }
        index += 1
        acts.append(act)

    case_data['acts'] = acts
    case_data['meetings'] = meetings

    print('MEETINGS: ', meetings)
    if case_data['act_file_url']:
        context.emit(rule='download', data={'act_file_url': case_data['act_file_url'],
                                            'case_url': case_data['case_url']})
    print('CASE_DATA: ', case_data['case_url'])
    # print('CASE URL)
    context.emit(rule='store', data=case_data)


# def get_act_file_url(page):
#     file_url = page.html.xpath(const.ACT_FILE_URL)
#     if len(file_url) > 0:
#         return const.BASE_URL + file_url[0]
#     return None


def get_data(page, param):
    try:
        if param == 'Суд':
            return page.html.xpath("//th[contains(text(), '{}')]/following-sibling::td/text()".format(param))[1].strip()
        else:
            return page.html.xpath("//th[contains(text(), '{}')]/following-sibling::td/text()".format(param))[0].strip()
    except IndexError as ie:
        print(ie)


def get_meeting_info(page, index, param_num):
    try:
        return merge_list(page.html.xpath("//div[@id='meetings']//tbody/tr[{}]/td[{}]//text()".format(index, param_num)))
    except IndexError as ie:
        print(ie)


def get_act_info(page, index, param_num):
    try:
        return merge_list(page.html.xpath("//div[@id='acts']//tbody/tr[{}]/td[{}]//text()".format(index, param_num)))
    except IndexError as ie:
        print(ie)


def get_act_download_url(page):
    try:
        return const.BASE_URL + page.html.xpath("//div[@id='acts']//a/@href")[0]
    except IndexError as ie:
        print(ie)


def merge_list(l):
    if len(l) > 1:
        return [''.join(e.strip()) for e in l][1]
    else:
        return [''.join(e.strip()) for e in l][0]
