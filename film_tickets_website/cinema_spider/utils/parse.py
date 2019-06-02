import re
import json
import requests as rq


def request_and_parse(url, params, headers):
    res = rq.get(url=url, params=params, headers=headers)
    text = parse_res_to_result(res)
    return text


def request_without_pa_and_parse(url, headers):
    res = rq.get(url=url, headers=headers)
    text = parse_res_to_result(res)
    return text


def parse_res_to_result(res):
    if res.status_code == 200:
        return res.text
    return None


def extract_json(text,pattern):
    text_json = re.search(pattern, text, re.S).group(1)
    return json.loads(text_json)


def parse_to_movie(movie_json):
    from cinema_spider.models.movie import Movie
    id = movie_json.get('id')
    img = movie_json.get('img')
    nm = movie_json.get('nm')
    is_released = movie_json.get('globalReleased')
    release_time = movie_json.get('rt')
    score = movie_json.get('sc')
    show_info = movie_json.get('showInfo')
    showst = movie_json.get('showst')
    star = movie_json.get('star')
    version = movie_json.get('version')
    wish_count = movie_json.get('wish')
    if id:
        return Movie(
            id=id,
            img=img,
            nm=nm,
            globalReleased=is_released,
            rt=release_time,
            sc=score,
            showInfo=show_info,
            showst=showst,
            star=star,
            version=version,
            wish=wish_count
        )
    else:
        return None
