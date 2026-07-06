import psycopg2
import os
import logging
from datetime import datetime

from psycopg2 import extras
from dotenv import load_dotenv

load_dotenv()


class DataBase:
    def __init__(self):
        self.connection = self._connect()
        logging.info('Подключение к бд выполнено успешно')


    # Connect to DB
    def _connect(self):
        return psycopg2.connect(
            database=os.getenv("DB_FOR_PROJECT"),
            host=os.getenv("POSTGRES_HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )


    # SQL command
    # insert command
    def add_in_db(self, date: str , dollar_rate: float):
        try:
            if not date or not dollar_rate:
                raise ValueError("Need data in func - add_in_db")

            sql_query = """
                INSERT INTO dollar_by_data (d_date, dollar_rate)
                VALUES (%s, %s)
                ON CONFLICT (d_date) DO NOTHING
            """

            with self.connection.cursor() as cursor:
                cursor.execute(
                    sql_query, 
                    (date, dollar_rate)
                )
                self.connection.commit()
        
        except Exception as e:
            logging.error(f"Ошибка при единичной вставки в бд - {e}")
    

    def add_many_in_db(self, data_list: list[tuple[str, float]]):
        try:
            if not data_list:
                raise ValueError("Need data in func - add_many_in_db")
        
            sql_query = """
                INSERT INTO dollar_by_data (d_date, dollar_rate)
                VALUES %s
                ON CONFLICT (d_date) DO NOTHING
            """

            with self.connection.cursor() as cursor:
                extras.execute_values(
                    cursor,
                    sql_query,
                    data_list
                )
                self.connection.commit()
                logging.info(f'В базу данных {os.getenv("DB_FOR_PROJECT")}, таблицу dollar_by_data успешно произведенна вставка')
        
        except Exception as e:
            logging.error(f'Ошибка во множественно вставке в БД - {e}')


    # get data command
    def get_rate_by_data(self, date: datetime):
        try:
            postgres_date = self.get_postgres_type_date(date)

            sql_query = """
                SELECT d.dollar_rate as rate FROM dollar_by_data as d
                WHERE d.d_date = %s;
            """

            with self.connection.cursor() as cursor:
                cursor.execute(sql_query, (postgres_date, ))
                result = cursor.fetchone()
                return result[0] if result else None

        except Exception as e:
            logging.error(f"Ошибка при обращении к бд за данными - {e}")


    # Help command
    def get_postgres_type_date(self, date):
        return datetime.strftime(date, '%Y-%m-%d')
        return None


    # Close
    def close(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()

        logging.info('Соединение с бд закрыто')
        

    def __del__(self):
        self.close()
