class Cinema:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('nm')
        self.address = kwargs.get('addr')
        self.show_times = kwargs.get('showTimes')
        self.hall_type = kwargs.get('hallType')


class CinemaOfMovie(Cinema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.movies=kwargs.get('movies')


class CinemaDetail:
    def __init__(self,**kwargs):
        self.id=kwargs.get('cinemaId')
        self.name=kwargs.get('cinemaName')

if __name__ == '__main__':
    a=CinemaOfMovie(id=1,nm=2,sellPrice=3)
    print(a.__dict__)