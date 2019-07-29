import re
from lxml import html
from aiohttp import web, ClientSession
from aiohttp.web_request import Request
from yarl import URL

PROXY_ADDRESS = 'http://127.0.0.1:8080'
INCLUDE_HEADERS = ['accept', 'accept-encoding', 'accept-charset', 'content-type', 'user-agent']

def filter_headers(headers):
    _headers = {}
    for header, value in headers.items():
        if header.lower() in INCLUDE_HEADERS:
            _headers[header] = value
    print(_headers)
    return _headers


def process_link(el, attr_name):
    if attr_name in el.attrib:
        el.attrib[attr_name] = el.attrib[attr_name].replace('https://habr.com', PROXY_ADDRESS)


def process_text(el):
    pattern = r'\b([а-яёa-z]{6})\b'
    exclude_tags = ['script', 'style', 'noscript', 'meta', 'link', 'code']
    if el.tag not in exclude_tags:
        if el.text:
            el.text = re.sub(pattern, r'\1™', el.text, flags=re.IGNORECASE)
        if el.tail:
            el.tail = re.sub(pattern, r'\1™', el.tail, flags=re.IGNORECASE)

def process_habr_page(habr_html: str):
    root = html.fromstring(habr_html)

    for el in root.iter():
        process_text(el)
        if el.tag == 'a':
            process_link(el, 'href')
        if el.tag == 'use':
            process_link(el, 'xlink:href')
    page = html.tostring(root, encoding='unicode')
    page = page.replace('&amp;plus;', '+')  # dirty hack; possibly lxml lib have broken serialization
    return page


async def fetch_habr_page(session: ClientSession, rel_url: URL, headers):
    url = f'https://habr.com{rel_url}'
    async with session.get(url, headers=headers) as response:
        content = await response.read()
        response_headers = filter_headers(response.headers)
        if 'text/html' in response_headers['Content-Type']:
            content = content.decode('utf-8')
            return process_habr_page(content), response_headers
        return content, response_headers



async def handler(request: Request):
    rel_url = request.rel_url
    async with ClientSession() as session:
        content, response_headers = await fetch_habr_page(session, rel_url, filter_headers(request.headers))
        return web.Response(body=content, headers=response_headers)


def init_app(argv):
    app = web.Application()
    app.add_routes([web.get('/{tail:.*}', handler), ])
    return app
