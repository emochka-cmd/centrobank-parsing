from parser import get_xml_content_from_page
import generator
import db 
from datetime import datetime

def pipeline():
    postgres_db = db.DataBase()

    all_data = generator.get_all_data()
    many_in_db = [] #  list[tuple[str, float]]

    for data in all_data:
        url = generator.generate_url(data)
        
        dollar_rate = get_xml_content_from_page(url)
        dollar_rate = float(dollar_rate.replace(',', '.'))

        curr_row = (data, dollar_rate)
        print(curr_row)
        many_in_db.append(curr_row)

    postgres_db.add_many_in_db(many_in_db) 


if __name__ == "__main__":
    start = datetime.now()
    pipeline()
    end = datetime.now() - start
    print(end)