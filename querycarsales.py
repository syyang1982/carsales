import requests
from bs4 import BeautifulSoup


class carinfo(object):
    def __init__(self):
        self._title = None
        self._year = 0
        self._price = -999
        self._pricetype = None
        self._explorelink = None
        self._imagelink = None
        self.home = 'https://www.carsales.com.au'

    def set_title(self, value):
        self._title = value

    def get_title(self):
        return self._title

    def del_title(self):
        del self._title

    title = property(get_title, set_title, del_title, "car title")

    def set_year(self, value):
        self._year = value

    def get_year(self):
        return self._year

    def del_year(self):
        del self._year

    year = property(get_year, set_year, del_year, "car year")

    def set_price(self, value):
        self._price = value.replace(',', '')

    def get_price(self):
        return self._price

    def del_price(self):
        del self._price

    price = property(get_price, set_price, del_price, "car price")

    def set_pricetype(self, value):
        self._pricetype = value

    def get_pricetype(self):
        return self._pricetype

    def del_pricetype(self):
        del self._pricetype

    pricetype = property(get_pricetype, set_pricetype, del_pricetype, "car pricetype")

    def set_explorelink(self, value):
        self._explorelink = self.home + value

    def get_explorelink(self):
        return self._explorelink

    def del_explorelink(self):
        del self._explorelink

    explorelink = property(get_explorelink, set_explorelink, del_explorelink, "car explore link")

    def set_imagelink(self, value):
        self._imagelink = self.home + value

    def get_imagelink(self):
        return self._imagelink

    def del_imagelink(self):
        del self._imagelink

    imagelink = property(get_imagelink, set_imagelink, del_imagelink, "car imagelink")


if __name__ == '__main__':
    # this is the real url to get car data. filtering with price low to high and show 48 models
    carmodel = ['Hatch', 'Sedan', 'SUV', 'Wagon', 'UTE']
    car = carmodel[2]

    # carurl = ('https://www.carsales.com.au/new-cars/model-filter/'
    #           'models?bodyStyles=Wagon&requestType=CategoryLanding&limit=24'
    #           '&skip=0&minPrice=null&maxPrice=null&sort=price-low-to-high')

    carurl = ('https://www.carsales.com.au/new-cars/model-filter/'
              'models?bodyStyles=' + car +
              '&requestType=CategoryLanding&limit=24'
              '&skip=0&minPrice=null&maxPrice=null&sort=price-low-to-HIGH')

    # if pretend as web browser, carsales will reject
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;", "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8", "Referer": "http://www.example.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}

    res = requests.get(carurl, headers=headers)

    # parse html
    cars = BeautifulSoup(res.text, 'html.parser')
    count = len(cars.select('._c-model-card__title'))
    carlist = list()

    for i in range(0, count):
        # () after carinfo is critical...
        carlist.append(carinfo())
        carlist[i].title = cars.select('._c-model-card__title')[i].text
        carlist[i].year = cars.select('._c-model-card__year')[i].text
        carlist[i].price = cars.select('._c-price__amount')[i].text[1:]
        carlist[i].pricetype = cars.select('._c-price__type')[i].text
        carlist[i].imagelink = cars.select('._c-model-card__thumb-image')[i]['src']
        carlist[i].explorelink = cars.select('._c-model-card__explore')[i]['href']

    file = car + '_info.csv'
    f = open(file, 'w')
    f.writelines('index, title,  year, price, pricetype, explorelink, imagelink\n')

    for i, c in enumerate(carlist):
        f.writelines(str(i) + ',' + c.title + ',' + c.year + ','
                     + c.price + ',' + c.pricetype + ','
                     + c.explorelink + ',' + c.imagelink + '\n')

    f.close()
