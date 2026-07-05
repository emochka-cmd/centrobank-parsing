import xml.etree.ElementTree as ET
import requests


DOLLAR_ID = 'R01235'


def get_xml_content_from_page(url: str):
    try:
        res = requests.get(url)
        res.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Ошбика в request запросе")
    
    root = ET.fromstring(res.content)
    value = root.find(f'./Valute[@ID="{DOLLAR_ID}"]')

    if value is None:
        raise KeyError("Валюта с ID R01235 не найдена в XML")

    value_node = value.find('Value')

    if value_node is None:
        raise ValueError("Тег <Value> пуст или отсутствует")
    
    return value_node.text


if __name__ == "__main__":
    res = get_content_from_page("https://cbr.ru/scripts/XML_daily.asp?date_req=04/07/2026")
    print(res)


