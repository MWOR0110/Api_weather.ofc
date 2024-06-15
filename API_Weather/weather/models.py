from django.db import models

class WeatherEntity:
    id = ''

    def __init__(self, temperature, date,
                 city='', atmosphericPressure='',
                 humidity='', weather='', id = '') -> None:
        self.temperature = temperature
        self.city = city
        self.atmosphericPressure = atmosphericPressure
        self.humidity = humidity
        self.weather = weather
        self.date = date
        self.id = id

    def __str__(self) -> str:
        return (f"Weather <{self.temperature}>")
