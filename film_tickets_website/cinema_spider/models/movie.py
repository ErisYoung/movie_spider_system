import re
from lxml import etree
from cinema_spider.models.person import Actor, Director
from cinema_spider.utils import get_current_date_str, request_and_parse, extract_json, request_without_pa_and_parse

regex_pattern_api = r"= (.*?);var"
regex_pattern_stills = r'"stagepicture":\[(.*?),{"screenshotstageimage"'
movie_detail_url = "http://movie.mtime.com/{id}/"
movie_stills_url = "http://movie.mtime.com/{id}/posters_and_images/stills/hot.html"
movie_all_stills_url = "http://movie.mtime.com/{id}/posters_and_images/"
movie_detail_API_url = "http://service.library.mtime.com/Movie.api"
FULL_CREDITS_SUFFIX = "/fullcredits.html"
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

MTIME_STILLS_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "DefaultCity-CookieKey=974; DefaultDistrict-CookieKey=0; _tt_=B1E59E563EAE1DDBFB19BD6C5B961440; __utma=196937584.583284690.1559266681.1559266681.1559266681.1; __utmz=196937584.1559266681.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; maxShowNewbie=2; _userCode_=201953193882350; _userIdentity_=201953193884540; SearchTrack=TrackId=38dd948f-f374-48f7-9106-524cfc44daf9; searchHistoryCookie=%u76D7%u68A6%u7A7A%u95F4%2C%u590D%u4EC7%u8005%u8054%u76DF; _movies_=83336.218090; Hm_lvt_6dd1e3b818c756974fb222f0eae5512e=1559266681,1559267575,1559267586,1559283800; _utmx_=PnChBIExINJjVrTwvlq92AFc4ILk55O7wKOPODZrBeY=; SearchAction=ActionId=6d881441-6423-4466-b1eb-b4a599294dc1&SearchTextMd5=f7cf3b4eab223bacbfda798ec6b018d9; Hm_lpvt_6dd1e3b818c756974fb222f0eae5512e=1559283805",
    "Host": "movie.mtime.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

MTIME_HTML_HEADERS = {
    "Upgrade-Insecure-Requests": "1",
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
        self.directors = self.get_directors_cls()
        self.actors = self.get_actors_cls()
        self.movie_rating = kwargs.get('movieRating')
        self._params_init()

    def _params_init(self):
        MTIME_SERVICE_HEADERS.update({"Referer": self.url})

    def __repr__(self):
        return f"<Movie<{self.id},{self.title}>>"

    def parse_to_director_api(self, director_str):
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
    def parse_to_actor_api(actor_list):
        if not actor_list:
            return None
        for item in actor_list:
            actor = Actor(**item)
            yield actor

    def get_mid_from_url(self):
        return self.url.split("/")[-2]

    def get_movie_box_office(self):
        movie_detail_params = {
            "Ajax_CallBack": "true",
            "Ajax_CallBackType": "Mtime.Library.Services",
            "Ajax_CallBackMethod": "GetMovieOverviewRating",
            "Ajax_CrossDomain": "1",
            "Ajax_RequestUrl": self.url,
            "t": get_current_date_str(),
            "Ajax_CallBackArgument0": self.get_mid_from_url()
        }

        text = request_and_parse(url=movie_detail_API_url, params=movie_detail_params, headers=MTIME_SERVICE_HEADERS)
        result = extract_json(text, regex_pattern_api)
        return result

    @staticmethod
    def extract_movie_detail(text):
        html = etree.HTML(text)
        directors = html.xpath('//dl[@class="info_l"]/dd[1]/a')
        dir_dict = {}
        temp_dict, temp_list = {}, []
        for director in directors:
            temp_dict['name'] = director.xpath("./text()")[0]
            temp_dict['url'] = director.xpath("./@href")[0]
            temp_list.append(temp_dict.copy())

        introduce = html.xpath('//dl[@class="info_l"]/dt/p[1]/text()')[0]
        dir_dict['director'] = temp_list
        dir_dict['introduce'] = introduce
        return dict(extra=dir_dict)

    def parse_movie_detail(self):
        url = self.url
        text = request_and_parse(url=url, params=None, headers=MTIME_HTML_HEADERS)
        date_dict = self.extract_movie_detail(text)
        return date_dict

    def parse_all_director_to_list(self):
        url = self.url
        text = request_and_parse(url=url, params=None, headers=MTIME_HTML_HEADERS)
        html = etree.HTML(text)
        directors = html.xpath('//dl[@class="info_l"]/dd[1]/a')
        temp_dict, temp_list = {}, []
        for director in directors:
            temp_dict['name'] = director.xpath("./text()")[0]
            temp_dict['url'] = director.xpath("./@href")[0]
            temp_list.append(temp_dict.copy())
        return temp_list

    def generate_director(self, dir_list):
        for item in dir_list:
            yield Director(nameCn=item.get('name'), personUrl=item.get('url'), id=self.id)

    def get_directors_cls(self):
        dirs_list = self.parse_all_director_to_list()
        dirs_cls = self.generate_director(dirs_list)
        return dirs_cls

    def parse_all_actor_to_list(self):
        url = self.url + FULL_CREDITS_SUFFIX
        text = request_and_parse(url=url, params=None, headers=MTIME_HTML_HEADERS)
        html = etree.HTML(text)
        main_actors = html.xpath('//div[@class="db_actor"]/dl[1]/dd')
        temp_dict, temp_list = {}, []
        for actor in main_actors:
            temp_dict['img'] = actor.xpath(".//img/@src")[0]
            temp_dict['name_cn'] = actor.xpath(".//h3/a/text()")[0]
            temp_dict['name_en'] = actor.xpath(".//p/a/text()")[0]
            temp_dict['actor_url'] = actor.xpath(".//p/a/@href")[0]
            temp_dict['play_role'] = actor.xpath("./div[2]//h3/text()")[0]
            temp_list.append(temp_dict.copy())
        return temp_list

    def generate_actor(self, actor_list):
        for item in actor_list:
            yield Actor(
                nameCn=item.get('name_cn'),
                personUrl=item.get('actor_url'),
                img=item.get('img'),
                name_en=item.get('name_en'),
                play_role=item.get('play_role'),
                id=self.id
            )

    def get_actors_cls(self):
        actors_list = self.parse_all_actor_to_list()
        actors_cls = self.generate_actor(actors_list)
        return actors_cls

    def get_movie_detail_data(self):
        """
        get movie's detail date,contains introduce,main stars,director and so on
        entering function
        :return:
        """
        result = self.get_movie_box_office()
        result_detail = self.parse_movie_detail()
        result.update(result_detail)
        return result

    def get_movie_director_data(self):
        """
        get movie's director data,contains,actor_url,name_en,name_cn,play_role,img_url
        :return:
        """
        dir_list = self.parse_all_director_to_list()
        return dict(directors=dir_list)

    def get_movie_stars_data(self):
        """
        get movie's actors data,contains dir_name,dir_url
        :return:
        """
        actor_list = self.parse_all_actor_to_list()
        return dict(actors=actor_list)

    def get_movie_stills(self):
        """
        get movie's stills,contains img_id, img_220 ,img_1000,img_235
        :return:
        """
        url = movie_stills_url.format(id=self.id)
        text = request_and_parse(url=url, params=None, headers=MTIME_STILLS_HEADERS)
        result_json = extract_json(text, regex_pattern_stills)
        return result_json


if __name__ == '__main__':
    a = MovieMtime(movieUrl="http://movie.mtime.com/218090/", movieId="218090")
    print(a.get_movie_director_data())
