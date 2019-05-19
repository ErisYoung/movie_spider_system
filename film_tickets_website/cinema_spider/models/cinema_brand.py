class CityBrands:
    def __init__(self, **kwargs):
        self.city_belong = kwargs.get('city')
        self.cinema_brand_list = kwargs.get('cinema_brand_list')
        self.cinema_count = kwargs.get('count')

    def get_city_name(self):
        return self.city_belong

    def get_cinema_amount(self):
        count = 0
        for cinema_brand in self.cinema_brand_list:
            count += cinema_brand.get_cinema_brand_count()
        return count


class CinemaBrand:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.count = kwargs.get('count')

    def get_cinema_brand_count(self):
        return self.count
