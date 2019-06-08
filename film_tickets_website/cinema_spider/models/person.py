from lxml import etree
import threading
from cinema_spider.utils import request_and_parse, parse_list_length, parse_array_first, extract_json

AWARD_SUFFIX = "awards.html"
PHOTO_SUFFIX = "/photo_gallery/"
WORKS_SUFFIX = "/filmographies/"
NOT_EXISTS_KEY = "None"
regex_pattern_director_picture = r'imageList = (.*?)var'
DIRECTOR_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "DefaultCity-CookieKey=974; DefaultDistrict-CookieKey=0; _tt_=B1E59E563EAE1DDBFB19BD6C5B961440; maxShowNewbie=2; _userCode_=201953193882350; _userIdentity_=201953193884540; __utmz=196937584.1559381600.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; searchHistoryCookie=%u8D85%u611F%u730E%u6740%2C%u8096%u751F%u5BA2%u7684%u6551%u8D4E%2C%u8096%u7533%u7684%u6551%u8D4E%2C%u8096%u7533%u514B%u7684%u6551%u8D4E%2C%u590D%u4EC7%u8005%u8054%u76DF; __utma=196937584.583284690.1559266681.1559381600.1559461561.3; __utmz=28869693.1559474169.4.4.utmcsr=movie.mtime.com|utmccn=(referral)|utmcmd=referral|utmcct=/218090/; _movies_=10652.225337.12231.218090; Hm_lvt_6dd1e3b818c756974fb222f0eae5512e=1559381603,1559458474,1559471780,1559715908; Hm_lpvt_6dd1e3b818c756974fb222f0eae5512e=1559715908; __utma=28869693.1802983944.1559381773.1559478676.1559715908.6; __utmc=28869693; __utmb=28869693.2.10.1559715908",
    "Host": "people.mtime.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

MTIME_PEOPLE_HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "DefaultCity-CookieKey=974; DefaultDistrict-CookieKey=0; _tt_=B1E59E563EAE1DDBFB19BD6C5B961440; __utma=196937584.583284690.1559266681.1559266681.1559266681.1; __utmz=196937584.1559266681.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; maxShowNewbie=2; _userCode_=201953193882350; _userIdentity_=201953193884540; SearchTrack=TrackId=38dd948f-f374-48f7-9106-524cfc44daf9; searchHistoryCookie=%u76D7%u68A6%u7A7A%u95F4%2C%u590D%u4EC7%u8005%u8054%u76DF; _movies_=83336.218090; Hm_lvt_6dd1e3b818c756974fb222f0eae5512e=1559266681,1559267575,1559267586,1559283800; _utmx_=PnChBIExINJjVrTwvlq92AFc4ILk55O7wKOPODZrBeY=; SearchAction=ActionId=6d881441-6423-4466-b1eb-b4a599294dc1&SearchTextMd5=f7cf3b4eab223bacbfda798ec6b018d9; Hm_lpvt_6dd1e3b818c756974fb222f0eae5512e=1559283805",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}


class Person:
    def __init__(self, **kwargs):
        self.name = kwargs.get('nameCn')
        self.person_url = kwargs.get('personUrl')
        self.belong_movie_id = kwargs.get('id')


class Actor(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img = kwargs.get('img')
        self.name_en = kwargs.get('name_en')
        self.play_role = kwargs.get('play_role')


class Director(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def request_with_url(url):
        text = request_and_parse(url=url, params=None, headers=DIRECTOR_HEADERS)
        html = etree.HTML(text)
        return html

    @staticmethod
    def get_award_detail(items):
        if not items:
            return NOT_EXISTS_KEY
        items_list = []
        temp_dict = {}
        for item in items:
            temp_dict['time'] = parse_array_first(item.xpath('./a[1]/text()'))
            temp_dict['award_name'] = parse_array_first(item.xpath('./span/text()'))
            temp_dict['award_movie'] = parse_array_first(item.xpath('./a[2]/text()'))
            temp_dict['movie_url'] = parse_array_first(item.xpath('./a[2]/@href'))
            items_list.append(temp_dict.copy())
        return items_list

    def get_award_data(self):
        html = self.request_with_url(self.person_url + AWARD_SUFFIX)
        winning_number, nomination_number = html.xpath('//h3[@class="per_awardstit"]/strong/text()')

        awards = html.xpath('//div[@id="awardInfo_data"]/dd')
        items_list = []
        temp_dict = {}
        for award in awards:
            temp_dict['aw_name'] = award.xpath('.//b/text()')[0]
            temp_dict['aw_wn'], temp_dict['aw_nn'] = parse_list_length(award.xpath('.//strong/text()'))
            aw_w_items = award.xpath(f'.//dd[not(@festivalid)][position()<{int(temp_dict["aw_wn"])+1}]')
            aw_n_items = award.xpath(f'.//dd[not(@festivalid)][position()>{temp_dict["aw_wn"]}]')
            temp_dict['winning_awards'] = self.get_award_detail(aw_w_items)
            temp_dict['nomination_awards'] = self.get_award_detail(aw_n_items)
            items_list.append(temp_dict.copy())
        return dict(total_wn=winning_number, total_nn=nomination_number, awards=items_list)

    def get_photo_data(self):
        url = self.person_url + PHOTO_SUFFIX
        text = request_and_parse(url=url, params=None, headers=MTIME_PEOPLE_HEADERS)
        result_json = extract_json(text, regex_pattern_director_picture)
        return result_json

    def get_work_data(self):
        html = self.request_with_url(self.person_url +WORKS_SUFFIX)
        movie_items=html.xpath('//div[@class="per_rele_list"]//dd')
        items_list = []
        temp_dict=temp_dict_item = {}
        for items in movie_items:
            temp_dict['year']=items.xpath('./i/text()')[0]
            for item in items.xpath("./div"):
                pass
                # temp_dict_item['cover_img']
                # temp_dict_item['movie_name']
                # temp_dict_item['movie_url']
                # temp_dict_item['score']
                # temp_dict_item['role']
                # temp_dict_item['role']


            temp_dict['movies']=temp_dict_item



    def get_detail_data(self):
        html = self.request_with_url(self.person_url)
        # html = self.request_with_url("http://people.mtime.com/903229/photo_gallery/")
        name_en = html.xpath('//p[@class="enname"]/text()')[0]
        person_job = html.xpath('//p[@class="mt9 __r_c_"]/text()')[0]
        head_photo = html.xpath('//div[@class="per_cover __r_c_"]//img/@src')[0]
        born_date, country = html.xpath('//dl[@class="per_base_born __r_c_"]/dd/text()')
        introduction = html.xpath('//div[@class="per_rmod per_info __r_c_"]/p[1]/text()')[0]

        # json_data = {
        #                 "name_cn": self.name,
        #                 "name_en": name_en,
        #                 "head_photo_url": head_photo,
        #                 "person_job": person_job,
        #                 "born_date": born_date.strip(),
        #                 "country": country.strip(),
        #                 "introduction": introduction,
        #                 "award": self.get_award_data(),
        #                 "works":,
        #             "pictures": self.get_photo_data()
        # }
        # return json_data


if __name__ == '__main__':
    d = Director(nameCn="安东尼·罗素", personUrl="http://people.mtime.com/892845/", id="892845")
    print(d.get_photo_data())
