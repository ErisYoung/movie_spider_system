# movie_spider_system
👻one movie spider and movie manage website

## Updating...

## Ins&Env

```bash
git clone git@github.com:ErisYoung/movie_spider_system.git
cd movie_spider_system
pip install -r requirements.txt
cd film_tickets_website\cinema_spider\spiders
python run.py
```

## Usage

#### get all cities' id:

    example:
    http://127.0.0.1:5000/allCities/

#### get cinema list:

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
        
#### get cinemas' list of specified movie

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
        
#### get showing movie list

    example:
    http://127.0.0.1:5000/movieOnInfoList?offset=12
    params:
         offset: offset, default 12 items, return 0-11
         
       
#### get showing movies list
    
    example:
    http://127.0.0.1:5000/moveComingList?offset=10
    params:
        offset: offset,default 10 items,return 0-9
    

#### get cinema's detail

    example:
    http://127.0.0.1:5000/cinemaDetail?cinemaId=25989
    params:
        cinemaId: cinema id
        

#### get new photo size

    example:
    http://127.0.0.1:5000/photoSize?photoUrl=http://p0.meituan.net/movie/67044d5479f075a18adba35571cadc4f978021.jpg&width=200&height=200
    params:
        photoUrl: origin url
        width: need photo width, can use width only to control new size due to proportion of lock
        height:        