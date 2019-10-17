from requests import RequestException
import kg_act_sot.constants as const


def fetch_links(context, data):
    context.log.info('\n*********\ncurrent page: %s\n*********' % const.PAGE_NUMBER)
    response = _initiate_session(context, data, const.SEED_PAGE_URL + '&page=%i' % const.PAGE_NUMBER)
    links = response.html.xpath(const.LINKS_XPATH)
    if len(links) == const.LINKS_COUNT:
        const.PAGE_NUMBER += 1
        context.recurse()
    _emit_links(context, links)


def _emit_links(context, links):
    # link example: /ru/delo/179829
    for link in links:
        data = {'case_url': const.BASE_URL + link}
        context.emit(rule='case_url', data=data)


def fetch_case_page(context, data):
    case_page = _initiate_session(context, data, data['case_url'])
    _emit_page(context, data, case_page)


def _emit_page(context, data, case_page):
    data['case_page'] = case_page.serialize()
    context.emit(rule='case_page', data=data)


def _initiate_session(context, data, url):
    attempt = data.pop('retry_attempt', 1)
    try:
        context.http.reset()
        result = context.http.get(url, lazy=True)

        if not result.ok:
            err = (result.url, result.status_code)
            context.emit_warning("Fetch fail [%s]: HTTP %s" % err)
            if not context.params.get('emit_errors', False):
                return
        else:
            context.log.info("Fetched [%s]: %r to get session data",
                             result.status_code,
                             result.url)
            return result

    except RequestException as ce:
        retries = int(context.get('retry', 3))
        if retries >= attempt:
            context.log.warn("Retry: %s (error: %s)", url, ce)
            data['retry_attempt'] = attempt + 1
            context.recurse(data=data, delay=2 ** attempt)
        else:
            context.emit_warning("Fetch fail [%s]: %s" % (url, ce))


def _fetch_post(context, data, url, formdata):
    attempt = data.pop('retry_attempt', 1)
    try:
        result = context.http.post(url, data=formdata)

        if not result.ok:
            err = (result.url, result.status_code)
            context.emit_warning("Fetch with post fail [%s]: HTTP %s" % err)
            if not context.params.get('emit_errors', False):
                return
        else:
            context.log.info("Fetched with post [%s]: %r",
                             result.status_code,
                             result.url)
            context.log.debug("Fetched with post [%s]: %r Post form data: %s",
                              result.status_code,
                              result.url,
                              str(formdata))
            return result

    except RequestException as ce:
        retries = int(context.get('retry', 3))
        if retries >= attempt:
            context.log.warn("Retry: %s (error: %s)", url, ce)
            data['retry_attempt'] = attempt + 1
            context.recurse(data=data, delay=2 ** attempt)
        else:
            context.emit_warning("Fetch fail [%s]: %s" % (url, ce))
