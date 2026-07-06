from parser import get_rate_from_single_page, get_dollar_rate_async
import generator
import db 


import asyncio
import aiohttp
import random
import logging
import os
import csv
from tqdm.asyncio import tqdm_asyncio

from datetime import datetime


# Работа с файлами
def csv_save(massive: list):
    current_date = datetime.now().strftime('%d.%m.%Y-%H:%M')

    file_path = f'data/csv_saves-{current_date}.csv'
    os.makedirs('data', exist_ok=True)

    with open(file_path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(massive)
    
    logging.info(f"Произведена запись в файл {file_path}")
    return file_path


# Работа с интернет парсингом
async def get_csv_with_dollar_rate():
    """data format - %d/%m/%Y
    dollar format - float
    """
    all_dates = generator.get_all_data()
    logging.info(f"Полученно {len(all_dates)} дат.")
    semaphore = asyncio.Semaphore(5)

    async def fetch(session, date):
        await asyncio.sleep(random.uniform(0.05, 0.2))
        async with semaphore:
            return await get_dollar_rate_async(
                session=session,
                date_str=date
            )

    async with aiohttp.ClientSession() as client:
        task = [fetch(client, url) for url in all_dates]
        result = await tqdm_asyncio.gather(*task, desc="Загрузка курсов", unit="дата", colour="blue")

    valid_results = [(date, rate) for date, rate in result if rate is not None]
    logging.info(f"Получено курсов: {len(valid_results)} из {len(all_dates)}")

    file_path = csv_save(valid_results)
    logging.info(f"Сохраненно в {file_path}")
    return file_path


# Работа с локальным парсингом
def add_data_to_db_with_csv(file_path: str):
    data_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
    
        for row in reader:
            try:
                date_str, rate_str = row

                date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                rate_obj = float(rate_str)

                date_for_db = datetime.strftime(date_obj, '%Y-%m-%d')
                data_list.append((date_for_db, rate_obj))

            except (ValueError, IndexError) as e:
                logging.warning(f"Пропущена некорректная строка: {row}, ошибка: {e}")


    postgres_db = db.DataBase()
    
    if data_list:
        postgres_db.add_many_in_db(data_list)
    else:
        logging.warning("Нет данных для вставки в БД")

    postgres_db.close()

   
async def async_pipeline_to_all_data_parse():
    file_path_to_csv = await get_csv_with_dollar_rate()
    add_data_to_db_with_csv(file_path_to_csv)


def parse_only_curr_date_and_send_in_db():
    curr_date = generator.get_now_date()
    date_str, rate = get_rate_from_single_page(curr_date)
    
    date_obj = datetime.strptime(date_str, '%d/%m/%Y')

    if date_obj and rate:
        date_to_db = datetime.strftime(date_obj, '%Y-%m-%d')

        postgres_db = db.DataBase()
        postgres_db.add_in_db(
            date=date_to_db,
            dollar_rate=rate
        )
        logging.info(f'Одна запись добавлена в БД - {date_to_db, rate}')
        postgres_db.close()

    else: 
        logging.warning("Нет данных для вставки в БД")    


if __name__ == "__main__":
    start = datetime.now()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    #asyncio.run(async_pipeline())
    parse_only_curr_date_and_send_in_db()
    end = datetime.now() - start
    print(end)