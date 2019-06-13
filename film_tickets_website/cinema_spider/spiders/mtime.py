from urllib.parse import quote
from cinema_spider.utils import get_current_date_str, request_and_parse, extract_json
from cinema_spider.models import MovieMtime

regex_pattern_api = r"= (.*?);var"
movie_search_url = "http://search.mtime.com/search/?q="
movie_search_API_url = "http://service.channel.mtime.com/Search.api"
movie_detail_API_url = "http://service.library.mtime.com/Movie.api"

MTIME_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "DefaultCity-CookieKey=974; DefaultDistrict-CookieKey=0; _tt_=B1E59E563EAE1DDBFB19BD6C5B961440; __utma=196937584.583284690.1559266681.1559266681.1559266681.1; __utmz=196937584.1559266681.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; maxShowNewbie=2; _userCode_=201953193882350; _userIdentity_=201953193884540; SearchTrack=TrackId=38dd948f-f374-48f7-9106-524cfc44daf9; searchHistoryCookie=%u76D7%u68A6%u7A7A%u95F4%2C%u590D%u4EC7%u8005%u8054%u76DF; _movies_=83336.218090; Hm_lvt_6dd1e3b818c756974fb222f0eae5512e=1559266681,1559267575,1559267586,1559283800; _utmx_=PnChBIExINJjVrTwvlq92AFc4ILk55O7wKOPODZrBeY=; SearchAction=ActionId=6d881441-6423-4466-b1eb-b4a599294dc1&SearchTextMd5=f7cf3b4eab223bacbfda798ec6b018d9; Hm_lpvt_6dd1e3b818c756974fb222f0eae5512e=1559283805",
    "Host": "service.channel.mtime.com",
    "Referer": "http://search.mtime.com/search/?q=%E5%A4%8D%E4%BB%87%E8%80%85%E8%81%94%E7%9B%9F",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}


def parse_to_movies(movie_json):
    movie_result = movie_json.get('value').get('movieResult')
    for item in movie_result.get('moreMovies', []):
        movie_time = MovieMtime(**item)
        yield movie_time


def get_search_movie(movie_name):
    """
    structure searched movies generation
    :param movie_name:
    :return:
    """
    movie_search_params = {
        "Ajax_CallBack": "true",
        "Ajax_CallBackType": "Mtime.Channel.Services",
        "Ajax_CallBackMethod": "GetSearchResult",
        "Ajax_CrossDomain": "1",
        "Ajax_RequestUrl": movie_search_url + quote(movie_name),
        "t": get_current_date_str(),
        "Ajax_CallBackArgument0": movie_name,
        "Ajax_CallBackArgument1": "0",
        "Ajax_CallBackArgument2": "974",
        "Ajax_CallBackArgument3": "0",
        "Ajax_CallBackArgument4": "1"
    }
    text = request_and_parse(url=movie_search_API_url, params=movie_search_params, headers=MTIME_HEADERS)
    text_json = extract_json(text, regex_pattern_api)
    movies = parse_to_movies(text_json)
    return list(movies)


if __name__ == '__main__':
    a = get_search_movie("复仇者联盟")
    print(list(a))
