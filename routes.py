from crawlee.crawlers import PlaywrightCrawlingContext
from crawlee.router import Router

from constants import BASE_OPTIONS, EMAIL_REG, PHONE_REG
from utils import filter_data


router = Router[PlaywrightCrawlingContext]()


@router.default_handler
async def default_handler(context: PlaywrightCrawlingContext) -> None:
    """Обеспечивает первичную обработку стартовой страницы."""
    context.log.info(f'Старт с главной: {context.request.url}')
    await user_data_handler(context)


@router.handler('user_data')
async def user_data_handler(context: PlaywrightCrawlingContext) -> None:
    """Извлекает email и телефоны из контента страницы и найденных ссылок."""
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

    phones_list = filter_data(PHONE_REG, data_str)
    email_list = filter_data(EMAIL_REG, data_str)

    await context.push_data(
        {'url': url, 'emails': email_list, 'phones': phones_list}
    )

    await context.enqueue_links(**BASE_OPTIONS, label='user_data')
