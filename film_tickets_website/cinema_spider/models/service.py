class CinemaService:
    def __init__(self, **kwargs):
        self.service_list = kwargs.get('service_list')


class Service:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.count = kwargs.get('count')
