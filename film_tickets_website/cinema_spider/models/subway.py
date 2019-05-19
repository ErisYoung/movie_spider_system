class CitySubways:
    def __init__(self, **kwargs):
        self.subway_list = kwargs.get('subway_list')
        self.city_belong = kwargs.get('city')
        self.count = kwargs.get('count')


class Subway:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.station_list = kwargs.get('station_list')
        self.count = kwargs.get('count')

    def get_subway_cinema_amount(self):
        count = 0
        for station in self.station_list:
            count += station.get_cinema_amount()
        return count


class Station:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.count = kwargs.get('count')
        self.subway_belong = kwargs.get("subway")

    def get_cinema_amount(self):
        return self.count
