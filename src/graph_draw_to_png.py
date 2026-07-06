import pandas

import matplotlib 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import db

from datetime import datetime, timedelta


STANDART_TIMEDELTA = timedelta(days=1)
MAX_DOLLAR_RATE_IN_GRAPH = 120
GRID = True
MAX_ITERATION = 100000

class DrawPng:
    def __init__(self):
        self.figure, self.axes = plt.subplots()


    # Функции с возможными графиками
    def draw_dollar_rate_in_range(self,
        start_date: datetime,
        end_date: datetime
    ):
        dates = self.generate_dates(start_date, end_date)

        self._draw_sketch_for_dollar_rate(dates=dates)
        self._add_point_to_graph(dates=dates)


    # Методы для отрисовки круса доллара
    def _add_point_to_graph(self,
        dates: [datetime]
    ):
        point_to_add = dict()

        postges_db = db.DataBase()

        for date in dates:
            rate = postges_db.get_rate_by_data(date)
            if not rate:
                continue
            point_to_add[date] = rate

        postges_db.close()
        self.axes.plot(point_to_add.keys(), point_to_add.values(), marker="o", linestyle="-", color="b")


    def _draw_sketch_for_dollar_rate(self,
        dates: [datetime],
        max_dollar_rate: float=MAX_DOLLAR_RATE_IN_GRAPH,
        step_y_in_graph: int=50 
    ):
        self.axes.set_title(
            "Ruble-to-dollar exchange rate",
            fontsize=16,
            color="red",
            loc="center")

        self.axes.set_xlabel("Date")
        self.axes.set_ylabel("Exchange rate")
        self.axes.grid(GRID)

        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        self.axes.xaxis.set_major_locator(mdates.AutoDateLocator())

        self.axes.tick_params(axis='x', rotation=45)

        max_dollar_rate_for_grapd = self.round_up_to_50(int(max_dollar_rate))
        
        yticks = self.create_y_ticks_graph(max_dollar_rate_for_grapd, step_y_in_graph)
        ytickslabels = [str(y) for y in yticks]
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(ytickslabels)

        self.axes.set_xlim(min(dates), max(dates))
        self.axes.set_ylim(0, max_dollar_rate_for_grapd)
        
        
    # Вспомагательные функции
    def round_up_to_50(self, n):
        return ((n // 50) + 1) * 50  


    def create_y_ticks_graph(self, max:int, step:int):
        return [i for i in range(0, max+1, step)]


    def create_x_labels(self, dates: [datetime]):
        labels = []

        for date in dates:
            labels.append(datetime.strftime(date, "%d-%m-%Y"))

        return labels


    def generate_dates(self,
        start_date: datetime,
        end_date: datetime
    ):
        dates = []

        iteration = 0
        while start_date <= end_date and iteration < MAX_ITERATION:
            dates.append(start_date)

            start_date += STANDART_TIMEDELTA
            iteration += 1
        
        return dates
    

    # Для сохранения
    def save_images(self, file_name: str='dolar_rate.png', dpi=300):
        self.figure.savefig(file_name, dpi=dpi, bbox_inches='tight')


if __name__ == "__main__":
    draw = DrawPng()
    start_code = datetime.now()

    start = datetime.now() - timedelta(days=12000)
    end = datetime.now()

    draw.draw_dollar_rate_in_range(start, end)
    draw.save_images()

    end_code = datetime.now() - start_code
    print(end_code)


