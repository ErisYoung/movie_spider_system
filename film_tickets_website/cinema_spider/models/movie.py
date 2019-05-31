class Movie:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.img = kwargs.get('img')
        self.nm = kwargs.get('nm')
        self.isReleased = kwargs.get('globalReleased')
        self.releaseTime = kwargs.get('rt')
        self.score = kwargs.get('sc')
        self.showInfo = kwargs.get('showInfo')
        self.showst = kwargs.get('showst')
        self.star = kwargs.get('star')
        self.version = kwargs.get('version')
        self.wish = kwargs.get('wish')

    def __repr__(self):
        return f"<Movie<{self.id},{self.nm}>>"


class MovieDetail(Movie):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.albumImg = kwargs.get('albumImg')
        self.bingeWatch = kwargs.get('bingeWatch')
        self.cat = kwargs.get('cat')
        self.director = kwargs.get('dir')
        self.dra = kwargs.get('dra')
        self.distributions = kwargs.get('distributions')
        self.music_name = kwargs.get("musicName")
        self.musicStar = kwargs.get('musicStar')
        self.is_Sale = kwargs.get('onSale')
        self.oriLang = kwargs.get('oriLang')
        self.photos = kwargs.get('photos')
        self.make_country = kwargs.get('src')
        self.pre_video = kwargs.get('vd')
        self.watched = kwargs.get('watched')

    def get_movie_showing(self):
        pass
