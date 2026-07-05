import xml.etree.ElementTree as ET
import requests
import generator

import aiohttp
import asyncio
import logging
import random


DOLLAR_ID = 'R01235'
MAX_ATTEMPT = 8


async def get_dollar_rate_async(session: aiohttp.ClientSession, date_str: str):
    url = generator.generate_url(date_str)
    send = False

    for attempt in range(MAX_ATTEMPT):
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                content = await resp.text()

                root = ET.fromstring(content)

                value = root.find(f'./Valute[@ID="{DOLLAR_ID}"]')

                if value is None:
                    return date_str, None

                value_node = value.find('Value')

                if value_node is None or value_node.text is None:
                    return date_str, None

                send = True
                rate = float(value_node.text.replace(',', '.'))
                return date_str, rate

        except Exception as e:
            wait = (2 ** attempt) + random.uniform(0.1, 0.5)
            logging.error(f"Ошибка при запросе {url}: {e}\nПовтор через - {wait}")
            await asyncio.sleep(wait)
            continue
    
    if not send:
        logging.warning(f'Данные с url не были спаршены.\nURL - {url}')
    
    return date_str, None


def get_xml_content_from_page(url: str):
    """
    Берет синхронно с url нужные данные
    """
    res = requests.get(url)

    if not res.ok:
        print(f"Не удалость обратиться к url - {url}")
        return None    
    
    root = ET.fromstring(res.content)
    value = root.find(f'./Valute[@ID="{DOLLAR_ID}"]')

    if value is None:
        print(f"Валюта с ID R01235 не найдена в XML по url - {url}")
        return None

    value_node = value.find('Value')

    if value_node is None:
        print(f"Нет значения валюты по url - {url}")
        return None
    
    rate = float(value_node.text.replace(',', '.'))
    return rate


if __name__ == "__main__":
    pass

