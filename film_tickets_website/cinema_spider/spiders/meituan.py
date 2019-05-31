import json
import math
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

cinema_list_base_url = "https://m.maoyan.com/ajax/cinemaList"
cinema_of_movie_base_url = "https://m.maoyan.com/ajax/movie?forceUpdate="
city_area_info_base_url = "https://m.maoyan.com/ajax/filterCinemas"
movies_now_showing_base_url = "https://m.maoyan.com/ajax/movieOnInfoList"
movies_showing_more_coming_base_url = "https://m.maoyan.com/ajax/moreComingList"
movie_detail_base_url = "https://m.maoyan.com/ajax/detailmovie"
cinema_detail_base_url = "http://m.maoyan.com/ajax/cinemaDetail"
MAX_BATCH_SIZE = 12
default_limit = 20


async def post(url, data):
    async with aiohttp.ClientSession() as session:
        res = await session.post(url, data=data, headers=HEADERS)
        return await res.json()


def get_cinema_list(city_id, **kwargs):
    """get a certain city,certain district and certain sub_area's cinemas

    :param city_id: city_id
    :param district_id: if get all district,then define it "-1"
    :param sub_area_id: if get all sub_area,then define it "-1"
    :param subway_id: if get all subway,then define it "-1"
    :param subway_station_id: if get all subway's stations,then define it "-1"
    :return: cinemas_list:json
    """
    cinema_api_params = {
        "day": str(get_current_date()),
        "offset": "0",
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


def get_all_showing_movies():
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
    return movie_list


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


def get_movie_detail(movie_id):
    movie_params = {
        'movieId': str(movie_id)
    }
    res = rq.get(url=movie_detail_base_url, params=movie_params, headers=HEADERS)
    return parse_res_to_result(res)


def get_cinema_detail(movie_id, cinema_id):
    cinema_params = {
        'cinemaId': str(cinema_id),
        'movieId': str(movie_id)
    }
    res = rq.get(url=cinema_detail_base_url, params=cinema_params, headers=HEADERS)
    return parse_res_to_result(res)


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


if __name__ == '__main__':
    # run()
    # get_all_showing_movies()
    # get_all_showing_movies()

    # print(get_cinema_list("40"))
    # print(get_cinema_of_movie_list("1207959", "57"))
    # get_all_cinemas_of_movie("1207959", "57")
    # print(get_cinema_detail("1207959", "922"))
    pass
