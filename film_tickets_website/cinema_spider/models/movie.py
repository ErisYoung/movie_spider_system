import re
from cinema_spider.models.person import Actor, Director
from cinema_spider.utils import get_current_date_str, request_and_parse, extract_json

movie_detail_API_url = "http://service.library.mtime.com/Movie.api"
MTIME_SERVICE_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "DefaultCity-CookieKey=974; DefaultDistrict-CookieKey=0; _tt_=B1E59E563EAE1DDBFB19BD6C5B961440; __utma=196937584.583284690.1559266681.1559266681.1559266681.1; __utmz=196937584.1559266681.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; maxShowNewbie=2; _userCode_=201953193882350; _userIdentity_=201953193884540; SearchTrack=TrackId=38dd948f-f374-48f7-9106-524cfc44daf9; searchHistoryCookie=%u76D7%u68A6%u7A7A%u95F4%2C%u590D%u4EC7%u8005%u8054%u76DF; _movies_=83336.218090; Hm_lvt_6dd1e3b818c756974fb222f0eae5512e=1559266681,1559267575,1559267586,1559283800; _utmx_=PnChBIExINJjVrTwvlq92AFc4ILk55O7wKOPODZrBeY=; SearchAction=ActionId=6d881441-6423-4466-b1eb-b4a599294dc1&SearchTextMd5=f7cf3b4eab223bacbfda798ec6b018d9; Hm_lpvt_6dd1e3b818c756974fb222f0eae5512e=1559283805",
    "Host": "service.library.mtime.com",
    "Referer": "http://movie.mtime.com/218090/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}


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
        self.english_name = kwargs.get('enm')
        self.albumImg = kwargs.get('albumImg')
        self.bingeWatch = kwargs.get('bingeWatch')
        self.movie_type = kwargs.get('cat')
        self.director = kwargs.get('dir')
        self.introduction = kwargs.get('dra')
        self.length = kwargs.get('dur')
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


class MovieMtime:
    def __init__(self, **kwargs):
        self.id = kwargs.get('movieId')
        self.title = kwargs.get('movieTitle')
        self.url = kwargs.get('movieUrl')
        self.cover = kwargs.get('cover')
        self.alias = kwargs.get('titleOthers')
        self.movie_length = kwargs.get('movieLength')
        self.movie_type = kwargs.get('genreTypes')
        self.director = self.parse_to_director(kwargs.get('directorHtml'))
        self.actors = list(self.parse_to_actor(kwargs.get('actors')))
        self.movie_rating = kwargs.get('movieRating')

    def __repr__(self):
        return f"<Movie<{self.id},{self.title}>>"

    def parse_to_director(self, director_str):
        if not director_str:
            return None
        dir_name, dir_url = self.regex_director_str(director_str)
        return Director(nameCn=dir_name, personUrl=dir_url)

    @staticmethod
    def regex_director_str(director_str):
        pattern = r'href="(?P<url>.*?)">(?P<name>.*?)</a>'
        result = re.search(pattern, director_str)
        return result.group("url"), result.group("name")

    @staticmethod
    def parse_to_actor(actor_list):
        if not actor_list:
            return None
        for item in actor_list:
            actor = Actor(**item)
            yield actor

    def get_mid_from_url(self):
        return self.url.split("/")[-2]

    def get_movie_detail_data(self):
        """
        get movie's detail date from API
        :return:
        """
        movie_detail_params = {
            "Ajax_CallBack": "true",
            "Ajax_CallBackType": "Mtime.Library.Services",
            "Ajax_CallBackMethod": "GetMovieOverviewRating",
            "Ajax_CrossDomain": "1",
            "Ajax_RequestUrl": self.url,
            "t": get_current_date_str(),
            "Ajax_CallBackArgument0": self.get_mid_from_url()
        }

        MTIME_SERVICE_HEADERS.update({"Referer": self.url})
        text = request_and_parse(url=movie_detail_API_url, params=movie_detail_params, headers=MTIME_SERVICE_HEADERS)
        result = extract_json(text)
        return result.get('value')

    def get_movie_director_data(self):
        pass

    def get_movie_stars_data(self):
        pass

    def get_movie_stills(self):
        pass


if __name__ == '__main__':
    a = MovieMtime(movieUrl="http://movie.mtime.com/218090/")
    print(a.get_movie_detail_data())
