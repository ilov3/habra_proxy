import re
from lxml import html
from aiohttp import web, ClientSession
from aiohttp.web_request import Request
from yarl import URL

PROXY_ADDRESS = 'http://127.0.0.1:8080'


def process_link(el, attr_name):
    if attr_name in el.attrib:
        el.attrib[attr_name] = el.attrib[attr_name].replace('https://habr.com', PROXY_ADDRESS)


def process_text(el):
    exclude_tags = ['script', 'style', 'noscript', 'meta', 'link', 'code']
    if el.tag not in exclude_tags and el.text:
        el.text = re.sub(r'\b([а-яёa-z]{6})\b', r'\1™', el.text, flags=re.IGNORECASE)


def process_habr_page(habr_html: str):
    root = html.fromstring(habr_html)

    for el in root.iter():
        process_text(el)
        if el.tag == 'a':
            process_link(el, 'href')
        if el.tag == 'use':
            process_link(el, 'xlink:href')
    return html.tostring(root, encoding='utf-8').decode()


async def fetch_habr_page(session: ClientSession, rel_url: URL):
    url = f'https://habr.com{rel_url}'
    async with session.get(url) as response:
        content = await response.read()
        try:
            content = content.decode()
        except UnicodeDecodeError:
            return content
        return process_habr_page(content)


async def handler(request: Request):
    rel_url = request.rel_url
    async with ClientSession() as session:
        data = await fetch_habr_page(session, rel_url)
        if isinstance(data, str):
            return web.Response(text=data, content_type='text/html')
        else:
            return web.Response(body=data)


def init_app(argv):
    app = web.Application()
    app.add_routes([web.get('/{tail:.*}', handler), ])
    return app
