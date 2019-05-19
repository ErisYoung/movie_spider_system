class CityDistricts:
    def __init__(self, **kwargs):
        self.district_list = kwargs.get('district_list')
        self.city_belong = kwargs.get('city')
        self.count = kwargs.get('count')


class District:
    def __init__(self, **kwargs):
        self.city_belong = kwargs.get('city')
        self.area_list = kwargs.get('area_list')
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.cinema_count = kwargs.get('count')

    def get_area_cinema_amount(self):
        count = 0
        for area in self.area_list:
            count += area.get_cinema_amount()
        return count


class Area:
    def __init__(self, **kwargs):
        self.count = kwargs.get('count')
        self.name = kwargs.get('name')
        self.id = kwargs.get('id')
        self.district_belong = kwargs.get('district')

    def get_cinema_amount(self):
        return self.count
