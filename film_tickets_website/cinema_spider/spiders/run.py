from flask import Flask, request
from flask import jsonify
from cinema_spider.spiders import get_all_cities, get_cinema_list, get_cinema_of_movie_list, get_movies_showing_offset

app = Flask(__name__)


@app.route('/')
def base():
    return "Welcome to COM's API!"


@app.route('/allCities/')
def all_cities():
    result_json = get_all_cities()
    print(result_json)
    return jsonify(result_json)


@app.route('/cinemaList')
def cinema_list():
    """get cinema list

    example:
    http://127.0.0.1:5000/cinemaList?day=2019-06-08&offset=20&districtId=-1&lineId=-1&areaId=-1&stationId=-1&cityId=50
    params:
        day: time, str
        offset: offset, default 20 items,return 0-19
        cityId: city code, example: 50（杭州）
        districtId: district code: 58 （江干区）
        areaId:  sub area code: 37228 （高沙商业街）
        lineId: subway code: 55 （一号线）
        stationId: subway station code: 1224 (凤起路)
    :return:
    """
    rq_args = request.args
    params = {
        "city_id": rq_args.get('cityId'),
        "offset": rq_args.get('offset'),
        "district_id": rq_args.get('districtId'),
        "subway_id": rq_args.get('lineId'),
        "sub_area_d": rq_args.get('areaId'),
        "subway_station_id": rq_args.get('stationId')
    }
    result_json = get_cinema_list(**params)
    return jsonify(result_json)


@app.route('/movie')
def cinemas_of_movie():
    """get cinemas list of specified movie

    example:
    http://127.0.0.1:5000/movie?movieId=344328&day=2019-06-08&offset=20&districtId=-1&lineId=-1&areaId=-1&stationId=-1&cityId=50
    params:
        movieId: movie_id
        day: time, str
        offset: offset, default 20 items,return 0-19
        cityId: city code, example: 50（杭州）
        districtId: district code: 58 （江干区）
        areaId:  sub area code: 37228 （高沙商业街）
        lineId: subway code: 55 （一号线）
        stationId: subway station code: 1224 (凤起路)
    :return:
    """
    rq_args = request.args
    params = {
        "movie_id": rq_args.get('movieId'),
        "city_id": rq_args.get('cityId'),
        "offset": rq_args.get('offset'),
        "district_id": rq_args.get('districtId'),
        "subway_id": rq_args.get('lineId'),
        "sub_area_d": rq_args.get('areaId'),
        "subway_station_id": rq_args.get('stationId')
    }
    result_json = get_cinema_of_movie_list(**params)
    return jsonify(result_json)


@app.route('/movieOnInfoList')
def showing_movies_list():
    """get showing movie list

    example:
    http://127.0.0.1:5000/movieOnInfoList?offset=12
    params:
         offset: offset, default 12 items, return 0-11
    :return:
    """
    rq_args = request.args
    params = {
        'offset': rq_args.get('offset')
    }
    result_json = get_movies_showing_offset(**params)
    return jsonify(result_json)


if __name__ == '__main__':
    app.run(debug=True)
