import re

from crawlee.crawlers import PlaywrightCrawlingContext
from crawlee.router import Router


router = Router[PlaywrightCrawlingContext]()


EXCLUDE_REG = [
    re.compile(r'.*\.pdf$', re.IGNORECASE),
    re.compile(r'.*(login|registration|auth|reset-password).*'),
    re.compile(r'.*\?.*'),
    re.compile(r'.*\.(jpg|jpeg|png|zip)$'),
]
EMAIL_REG = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REG = r'((?:\+7|8)[- _]*\(?\d{3}\)?[- _]*\d{3}[- _]*\d{2}[- _]*\d{2})'

BASE_OPTIONS = {
    'strategy': 'same-domain',
    'exclude': EXCLUDE_REG,
}


@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    context.log.info(f'Старт с главной: {context.request.url}')
    await user_data_handler(context)


@router.handler('user_data')
async def user_data_handler(context: PlaywrightCrawlingContext) -> None:
    context.log.info(f'Парсим страницу: {context.request.url}')

    url = context.request.url

    page_content = await context.page.content()

    links = await context.page.locator('a').all()
    link_list = []
    for link in links:
        href = await link.get_attribute('href')
        if href is not None:
            link_list.append(href.strip())

    links_str = ' '.join(link_list)

    data_str = page_content + ' ' + links_str

    def filter_emails(email_reg, email_str):
        emails = set(re.findall(email_reg, email_str))
        return list(emails) if emails else []

    def filter_phones(phone_reg, phone_str):
        phones = set(re.findall(phone_reg, phone_str))
        return list(phones) if phones else []

    phones_list = filter_phones(PHONE_REG, data_str)
    email_list = filter_emails(EMAIL_REG, data_str)

    await context.push_data(
        {'url': url, 'emails': email_list, 'phones': phones_list}
    )

    await context.enqueue_links(**BASE_OPTIONS, label='user_data')
