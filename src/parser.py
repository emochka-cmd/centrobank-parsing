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


def get_rate_from_single_page(date_str: str):
    """
    Берет синхронно с url нужные данные
    """
    url = generator.generate_url(date_str)

    try:
        res = requests.get(url)
        res.raise_for_status()

        root = ET.fromstring(res.content)
        value = root.find(f'./Valute[@ID="{DOLLAR_ID}"]')

        if value is None:
            logging.warning(f'Валюта с ID {DOLLAR_ID} не найдена для {date_str}')
            return date_str, None

        value_node = value.find('Value')
        if value_node is None or value_node.text is None:
            logging.warning(f'Тег Value отсутствует для {date_str}')
            return date_str, None

        rate = float(value_node.text.replace(',', '.'))
        return date_str, rate
    
    except Exception as e:
        logging.error(f'Данные с url не были спаршены.\nURL - {url}')

    return date_str, None


if __name__ == "__main__":
    pass

