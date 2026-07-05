from datetime import datetime, timedelta


START_DATE = datetime(day=1, month=7, year=1992)    #первая дата имещеюся в api центрабанка
#START_DATE = datetime(day=1, month=5, year=2026)
STANDART_DAYS_STEP = timedelta(days=1)
NOW_DATA = datetime.now()
MAX_ITERATION = 10000000


def get_all_data(
        start_date: datetime = START_DATE,
        step: timedelta = STANDART_DAYS_STEP
    ) -> list[str]:
    """will return all dates from 1992 to the current one"""
    all_data_list = list()
    current_date = START_DATE

    iteration = 0

    while current_date < NOW_DATA and iteration < MAX_ITERATION:
        format_date = datetime.strftime(current_date, '%d/%m/%Y')
        all_data_list.append(format_date)

        current_date = current_date + step
        iteration += 1

    return all_data_list


def generate_url(data: str) -> str:
    """get cbr url"""
    return f"https://cbr.ru/scripts/XML_daily.asp?date_req={data}"


def get_now_date() -> str:
    """return current date"""
    return datetime.strftime(NOW_DATA, '%d/%m/%Y')
    

if __name__ == "__main__":
    start = datetime.now()

    res = get_all_data()
    print(res)

    end = datetime.now() - start
    print(get_now_date())
    print(end)