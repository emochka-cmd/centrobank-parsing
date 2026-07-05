import psycopg2
import os

from psycopg2 import extras
from dotenv import load_dotenv

load_dotenv()


class DataBase:
    def __init__(self):
        self.connection = self._connect() 
        self.cursor_for_insert = self._create_insert_curcor()


    # Connect to DB
    def _connect(self):
        return psycopg2.connect(
            database=os.getenv("DB_FOR_PROJECT"),
            host=os.getenv("POSTGRES_HOST"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )


    def _create_insert_curcor(self):
        return self.connection.cursor()


    # SQL command
    def add_in_db(self, date: str , dollar_rate: float):
        if not date or not dollar_rate:
            raise ValueError("Need data in func - add_in_db")

        sql_query = """
            INSERT INTO dollar_by_data (d_date, dollar_rate)
            VALUES (%s, %s)
        """

        self.cursor_for_insert.execute(sql_query, (date, dollar_rate))
        self.connection.commit()

    
    def add_many_in_db(self, data_list: list[tuple[str, float]]):
        if not data_list:
            raise ValueError("Need data in func - add_many_in_db")
        
        sql_query = """
            INSERT INTO dollar_by_data (d_date, dollar_rate)
            VALUES %s
        """

        extras.execute_values(
            self.cursor_for_insert,
            sql_query,
            data_list
        )
        self.connection.commit()

        
    # Close
    def close(self):
        if hasattr(self, 'cursor_for_insert') and self.cursor_for_insert:
            self.cursor_for_insert.close()

        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
        

    def __del__(self):
        self.close()
