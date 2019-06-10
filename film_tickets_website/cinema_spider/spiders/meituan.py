import json
import math
import re
import time
import asyncio
import aiohttp
import requests as rq
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cinema_spider.utils import get_current_timestamp, get_current_date, get_timestamp_add
from cinema_spider.utils import store_dict_to_json, store_dict_to_serialization
from cinema_spider.utils import parse_to_movie

HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "_lxsdk_cuid=16a857b4247c8-003e73a55803da-58422116-144000-16a857b42481a; uuid_n_v=v1; iuuid=79F4B870761611E9A2B95115D7852D86390E1BA1522B4F3A9880417595ABFA4E; webp=true; selectci=true; _lx_utm=utm_source%3Dmeituanweb; __mta=208912045.1557017609572.1557819973854.1557832563343.8; _lxsdk=79F4B870761611E9A2B95115D7852D86390E1BA1522B4F3A9880417595ABFA4E; __mta=208912045.1557017609572.1557832563343.1557833162345.9; ci=50%2C%E6%9D%AD%E5%B7%9E; _lxsdk_s=16ab60e772e-be6-1fb-3ce%7C%7C30; latlng=34.0522342%2C-118.24368489999999%2C1557833411202",
    "Host": "m.maoyan.com",
    "If-None-Match": 'W/"207a-41vWzPaiZgOZJYkiuUVNfw"',
    "Referer": "https://m.maoyan.com/",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    "X-Requested-With": "XMLHttpRequest"
}
HTML_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "__mta=208912045.1557017609572.1559908507372.1559909287195.31; _lxsdk_cuid=16a857b4247c8-003e73a55803da-58422116-144000-16a857b42481a; uuid_n_v=v1; iuuid=79F4B870761611E9A2B95115D7852D86390E1BA1522B4F3A9880417595ABFA4E; selectci=true; webp=true; ci=10%2C%E4%B8%8A%E6%B5%B7; __mta=208912045.1557017609572.1559898905065.1559898942892.27; from=canary; __mta=208912045.1557017609572.1559898942892.1559907946559.28; _lxsdk=79F4B870761611E9A2B95115D7852D86390E1BA1522B4F3A9880417595ABFA4E; _lxsdk_s=16b31affffd-34e-76-86b%7C%7C49",
    "Host": "m.maoyan.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"

}

cinema_list_base_url = "https://m.maoyan.com/ajax/cinemaList"
cinema_of_movie_base_url = "https://m.maoyan.com/ajax/movie?forceUpdate="
cinema_detail_base_url = "http://m.maoyan.com/ajax/cinemaDetail"
city_area_info_base_url = "https://m.maoyan.com/ajax/filterCinemas"
movies_now_showing_base_url = "https://m.maoyan.com/ajax/movieOnInfoList"
movies_showing_more_coming_base_url = "https://m.maoyan.com/ajax/moreComingList"
movie_detail_base_url = "https://m.maoyan.com/ajax/detailmovie"
movie_detail_more_base_url = "http://m.maoyan.com/movie/{movie_id}?_v_=yes&channelId=4&$from=canary"
movies_not_showing_base_url = "http://m.maoyan.com/ajax/comingList"
MAX_BATCH_SIZE = 12
MAX_NOT_SHOWING_MOVIE_PAGE_SIZE = 10
default_limit = 20


async def post(url, data):
    async with aiohttp.ClientSession() as session:
        res = await session.post(url, data=data, headers=HEADERS)
        return await res.json()


def get_cinema_list(city_id, offset=0, date_str=get_current_date(), **kwargs):
    """get a certain city,certain district and certain sub_area's cinemas

    :param date_str: date string
    :param city_id: city_id
    :param offset: offset,default 20
    :param district_id: if get all district,then define it "-1"
    :param sub_area_id: if get all sub_area,then define it "-1"
    :param subway_id: if get all subway,then define it "-1"
    :param subway_station_id: if get all subway's stations,then define it "-1"
    :return: cinemas_list:json
    """
    cinema_api_params = {
        "day": date_str,
        "offset": str(offset),
        "limit": "20",
        "districtId": str(kwargs.get('district_id', "-1")),
        "lineId": str(kwargs.get("subway_id", "-1")),
        "hallType": "-1",
        "brandId": "-1",
        "serviceId": "-1",
        "areaId": str(kwargs.get("sub_area_id", "-1")),
        "stationId": str(kwargs.get("subway_station_id", "-1")),
        "item": "",
        "updateShowDay": "false",
        "reqId": str(get_current_timestamp()),
        "cityId": str(city_id),
        "lat": "34.0522342",
        "lng": "-118.24368489999999"
    }
    res = rq.get(url=cinema_list_base_url, params=cinema_api_params, headers=HEADERS)
    return parse_res_to_result(res)


async def get_more_cinema_of_movie_list(movie_id, city_id, offset=0, date_str=get_current_date(), **kwargs):
    """
    get specified movie of cinemas list
    :return:
    """
    current_timestamp = str(get_current_timestamp())
    cinema_movie_params = {
        "movieId": str(movie_id),
        "day": date_str,
        "offset": str(offset),
        "limit": "20",
        "districtId": str(kwargs.get('district_id', "-1")),
        "lineId": str(kwargs.get("subway_id", "-1")),
        "hallType": "-1",
        "brandId": "-1",
        "serviceId": "-1",
        "areaId": str(kwargs.get("sub_area_id", "-1")),
        "stationId": str(kwargs.get("subway_station_id", "-1")),
        "item": "",
        "updateShowDay": "false",
        "reqId": current_timestamp,
        "cityId": str(city_id),
        "lat": "34.0522342",
        "lng": "-118.24368489999999"
    }

    result = await post(url=cinema_of_movie_base_url + current_timestamp, data=cinema_movie_params)
    return result


def get_cinema_of_movie_list(movie_id, city_id, offset=0, date_str=get_current_date(), **kwargs):
    """
    get specified movie of cinemas list,single page,default 20 item
    :return:
    """
    current_timestamp = str(get_current_timestamp())
    cinema_movie_params = {
        "movieId": str(movie_id),
        "day": date_str,
        "offset": str(offset),
        "limit": "20",
        "districtId": str(kwargs.get('district_id', "-1")),
        "lineId": str(kwargs.get("subway_id", "-1")),
        "hallType": "-1",
        "brandId": "-1",
        "serviceId": "-1",
        "areaId": str(kwargs.get("sub_area_id", "-1")),
        "stationId": str(kwargs.get("subway_station_id", "-1")),
        "item": "",
        "updateShowDay": "false",
        "reqId": current_timestamp,
        "cityId": str(city_id),
        "lat": "34.0522342",
        "lng": "-118.24368489999999"
    }

    res = rq.post(url=cinema_of_movie_base_url + current_timestamp, data=cinema_movie_params)
    return parse_res_to_result(res)


def get_all_cinemas_of_movie(movie_id, city_id, date_str=get_current_date(), **kwargs):
    """
    get specified movie of cinemas list
    :param movie_id: movie_id
    :param city_id: city_id
    :param date_str: date_str
    :param kwargs:
    :return: cinema_list
    """
    base_cinema_json = get_cinema_of_movie_list(movie_id, city_id, 0, date_str, **kwargs)
    total = base_cinema_json.get('paging').get('total')
    cinema_list = base_cinema_json.get('cinemas', [])
    batch = math.ceil(total / default_limit)
    tasks = [asyncio.ensure_future(get_more_cinema_of_movie_list(movie_id, city_id, index * 20, date_str, **kwargs)) for
             index in range(1, batch)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        cinema_list.extend(task.result().get('cinemas', []))
    return cinema_list


def get_city_filter_cinema_info(city_id):
    """
    get city's district,service and other's type
    :param city_id:city_id
    :return:result:json
    """
    city_filter_params = {
        "ci": str(city_id)
    }
    res = rq.get(url=city_area_info_base_url, params=city_filter_params, headers=HEADERS)
    return parse_res_to_result(res)


def get_movies_now_showing():
    movies_now_params = {
        "token": ""
    }
    res = rq.get(url=movies_now_showing_base_url, params=movies_now_params, headers=HEADERS)
    return parse_res_to_result(res)


def get_movies_coming(movies_ids_str):
    movies_now_params = {
        "token": "",
        "movieIds": movies_ids_str,
    }
    result = rq.get(url=movies_showing_more_coming_base_url, params=movies_now_params, headers=HEADERS)
    return parse_res_to_result(result)


def get_movies_showing_offset(offset):
    """
    get movies which are now showing
    :param offset:
    :return:
    """
    offset = int(offset)
    base_movies_json = get_movies_now_showing()
    total = base_movies_json.get("total")
    if offset == MAX_BATCH_SIZE:
        movies = base_movies_json.get('movieList')
        new_movies = parse_img_to_real_url(movies)
        return dict(movies=new_movies, total=total)
    batch = math.ceil(offset / MAX_BATCH_SIZE)
    total_movies = base_movies_json.get("movieIds", [])
    current_movie_ids = total_movies[(batch - 1) * MAX_BATCH_SIZE:batch * MAX_BATCH_SIZE]
    result = get_movies_coming(current_movie_ids)
    movies = result.get('coming')
    new_movies = parse_img_to_real_url(movies)
    return dict(movies=new_movies, total=total)


async def get(url, params):
    async with aiohttp.ClientSession() as session:
        # 注意，使用aiohttp需要自己parse 多个参数，不会像request自动数组拼接
        res = await session.get(url, params=params, headers=HEADERS)
        return await res.json()


async def get_movies_more_coming(movies_ids_str):
    movies_now_params = {
        "token": "",
        "movieIds": movies_ids_str,
    }
    result = await get(url=movies_showing_more_coming_base_url, params=movies_now_params)
    return result


def get_movies_not_showing(city_id=50):
    """
    movies which will show
    :param city_id:
    :return:
    """
    movies_not_showing_params = {
        "ci": str(city_id),
        "token": "",
        "limit": "10",
    }
    res = rq.get(url=movies_not_showing_base_url, params=movies_not_showing_params, headers=HEADERS)
    return parse_res_to_result(res)


def get_more_movies_not_showing(movies_ids_str, city_id=50):
    movies_now_params = {
        "token": "",
        "ci": str(city_id),
        "limit": "10",
        "movieIds": movies_ids_str,
    }
    result = rq.get(url=movies_showing_more_coming_base_url, params=movies_now_params, headers=HEADERS)
    return parse_res_to_result(result)


def get_movies_not_showing_offset(offset, city_id=50):
    """
    get movies which will show
    :param offset: default 10 items per page
    :param city_id: city id
    :return:
    """
    offset = int(offset)
    base_movies_json = get_movies_not_showing(city_id)
    total_movies = base_movies_json.get("movieIds", [])
    total = len(total_movies)
    if offset == MAX_NOT_SHOWING_MOVIE_PAGE_SIZE:
        movies = base_movies_json.get('coming')
        new_movies = parse_img_to_real_url(movies)
        return dict(movies=new_movies, total=total)
    batch = math.ceil(offset / MAX_BATCH_SIZE)
    current_movie_ids = total_movies[
                        (batch - 1) * MAX_NOT_SHOWING_MOVIE_PAGE_SIZE:batch * MAX_NOT_SHOWING_MOVIE_PAGE_SIZE]
    result = get_more_movies_not_showing(current_movie_ids, city_id)
    movies = result.get('coming')
    new_movies = parse_img_to_real_url(movies)
    return dict(movies=new_movies, total=total)


def get_all_showing_movies():
    """
    获取当前所有上映电影的json
    :return:
    """
    base_movies_json = get_movies_now_showing()
    total = base_movies_json.get("total")
    total_movies = base_movies_json.get("movieIds", [])
    movie_list = base_movies_json.get("movieList", [])
    batch = math.ceil(total / MAX_BATCH_SIZE)
    current_movie_ids_list = [total_movies[i * MAX_BATCH_SIZE:(i + 1) * MAX_BATCH_SIZE] for i in range(1, batch)]
    tasks = [asyncio.ensure_future(get_movies_more_coming(movies_params_with_id(ids))) for ids in
             current_movie_ids_list]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    for task in tasks:
        movie_list.extend(task.result().get("coming", []))
    return dict(movies=movie_list)


def movies_params_with_id(movie_id_list):
    params_ids = "%2C".join(list(map(lambda x: str(x), movie_id_list)))
    return params_ids


def get_all_cities():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://maoyan.com/')
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"city-selected")]')))
    city_list = driver.execute_script('return localStorage.getItem("cities")')
    return json.loads(city_list)


def parse_img_to_real_url(movie_list):
    for item in movie_list:
        img = item.get('img')
        new_img = parse_photo_url_func(img)
        item.update({"img": new_img})
    return movie_list


def parse_photo_url_func(item):
    """
    stand by parse_photo_url func's map func param
    :param item:
    :return:
    """
    if isinstance(item, str):
        return item.replace("/w.h", "")
    elif isinstance(item, dict):
        new_avatar = parse_photo_url_func(item.get('avatar'))
        item.update({"avatar": new_avatar})
        return item


def parse_photo_url_real(photos):
    """
    get real photo's url
    :param photos:
    :return:
    """
    if isinstance(photos, list):
        new_photos = list(map(parse_photo_url_func, photos))
        return new_photos
    elif isinstance(photos, str):
        return parse_photo_url_func(photos)


def get_size_photo(photo_url, width, height):
    """
    get specified size of photo
    :param photo_url:
    :param width:
    :param height:
    :return:
    """
    photo_size_inter = "@{width}w_{height}h.webp"
    photo_url += photo_size_inter.format(width=width, height=height)
    return dict(url=photo_url, status="ok")


def get_movie_stars(movie_id):
    url = movie_detail_more_base_url.format(movie_id=movie_id)
    res = rq.get(url=url, headers=HTML_HEADERS)
    pattern = r'AppData = (.*?);</script>'
    result_json = re.search(pattern, res.text, re.S).group(1)
    stars_list = json.loads(result_json).get('celebrities')
    new_stars_list = parse_photo_url_real(stars_list)
    return new_stars_list


def get_movie_detail(movie_id):
    """
    get movie detail and merge movie's stars'detail to it.
    :param movie_id:
    :return:
    """
    movie_params = {
        'movieId': str(movie_id)
    }
    res = rq.get(url=movie_detail_base_url, params=movie_params, headers=HEADERS)
    temp_json = parse_res_to_result(res)
    photos = temp_json.get('detailMovie').get('photos', [])
    img = temp_json.get('detailMovie').get('img')
    new_photos = parse_photo_url_real(photos)
    new_img = parse_photo_url_real(img)
    stars_list = get_movie_stars(movie_id)
    temp_json.get('detailMovie').update({"img": new_img, "photos": new_photos, "stars_detail": stars_list})
    return temp_json


def get_cinema_detail(cinema_id):
    """
    get cinema detail
    :param cinema_id:
    :return:
    """
    cinema_params = {
        'cinemaId': str(cinema_id)
    }
    res = rq.get(url=cinema_detail_base_url, params=cinema_params, headers=HEADERS)
    temp_json = parse_res_to_result(res)
    movies = temp_json.get('showData').get('movies')
    new_movies = parse_img_to_real_url(movies)
    temp_json.get('showData').update({"movies": new_movies})
    return temp_json


def parse_res_to_result(res):
    if res.status_code == 200:
        return res.json()
    return None


def store_data_to_persistence(dict_data):
    store_dict_to_json(dict_data, "cities")
    store_dict_to_serialization(dict_data, "cities")


def parse_movie_generation(movie_list):
    for item in movie_list:
        yield parse_to_movie(item)


def handle_movie_list():
    movie_list = get_all_showing_movies()
    movie_generation = parse_movie_generation(movie_list)
    return movie_generation


def run():
    cities_data = get_all_cities()
    store_data_to_persistence(cities_data)


def store_one_json(data, file_name):
    store_dict_to_json(data, filename=file_name)


def get_json_file():
    a = get_movie_detail("1207959")
    store_dict_to_json(a, "movie_detail")

    b = get_city_filter_cinema_info("50")
    store_dict_to_json(b, "city_cinema_info")

    c = get_cinema_list("50")
    store_dict_to_json(c, "city_cinema_list")

    d = get_all_cinemas_of_movie("1207959", "57")
    store_dict_to_json(d, "cinemas_of_movie")


if __name__ == '__main__':
    # store_one_json(get_movies_not_showing(), "temp")
    store_one_json(get_movies_not_showing_offset("20"), "temp")
    # print(get_cinema_detail(""))
    # run()
    # print(get_all_cities())
    # get_all_showing_movies()

    # print(get_cinema_detail("1207959", "922"))
    # print(get_cinema_list("40"))
    # print(get_cinema_of_movie_list("1207959", "57"))
    # print(get_cinema_of_movie_list("1207959", "57"))
    # print(get_all_cinemas_of_movie("1207959", "57"))
    # get_json_file()

    # print(get_movie_detail("1207959"))

    # print(get_cinema_of_movie_list("1207959", "57",offset=20))
    # print(get_movies_showing_offset("24"))
