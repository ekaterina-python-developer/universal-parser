import asyncio
import re
from datetime import timedelta

from crawlee.crawlers import PlaywrightCrawler

from constants import URL_REG
from routes import router
from utils import collect_user_data


async def main() -> None:
    """Инициализирует краулер и выводит результат парсинга."""
    start_url = input('Введите адрес сайта: ').strip().strip('\'"')

    if not start_url:
        print('Вы ничего не ввели')
        return

    if not re.match(URL_REG, start_url):
        print('Ошибка: Введен некорректный URL! Обязательно https:// и домен.')
        return

    try:
        crawler = PlaywrightCrawler(
            headless=False,
            max_requests_per_crawl=10,
            request_handler=router,
            request_handler_timeout=timedelta(seconds=30),
        )
        await crawler.run([start_url])
        base_data = await crawler.get_data()

        final_result = {
            'url': start_url,
            'emails': collect_user_data(base_data.items, 'emails'),
            'phones': collect_user_data(base_data.items, 'phones'),
        }
        print('Парсинг завершён!')
        print(final_result)

    except Exception as e:
        print(f'Не удалось спарсить сайт. Ошибка: {e}')


if __name__ == '__main__':
    asyncio.run(main())
