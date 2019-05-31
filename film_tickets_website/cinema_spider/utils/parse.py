from cinema_spider.models import Movie


def parse_to_movie(movie_json):
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
