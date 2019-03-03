import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


def parsehtmltoDataFrame(txt):
    '''
    content: response content
    parse response content and store vehcile data to dataframe

    The vechicle feature data is located in the <div class="vehicle-feature">
    '''
    soup = BeautifulSoup(txt, 'html.parser')

    # find all vehicle title
    vehtitle = soup.find_all('h2')

    # the last one is not useful
    vehtitle.pop()
    vehtitle = [t.text for t in vehtitle]

    # get vehicle features
    vehfeatures = soup.find_all('div', class_='vehicle-features')

    odometers = []
    bodytype = []
    transmission = []
    engine = []

    for v in vehfeatures:
        tp = v.find_all('div', class_='feature-text')
        odometers.append(tp[0].text.split(" ")[0].replace(",", ""))
        bodytype.append(tp[1].text)
        transmission.append(tp[2].text)
        engine.append(tp[3].text)

    # get vehicle prices
    prices = soup.find_all('div', class_='price')
    prices.pop(0)
    pricelist = [a.text for a in prices]

    # get vehicle prices type
    pricetypes = soup.find_all('div', class_='price-desc')
    pricetypelist = [a.text for a in pricetypes]

    cardata = {}
    cardata['car title'] = vehtitle
    cardata['kms'] = odometers
    cardata['bodytype'] = bodytype
    cardata['engine'] = engine
    cardata['transmission'] = transmission
    cardata['price'] = pricelist
    cardata['price_type'] = pricetypelist

    return pd.DataFrame(cardata)

if __name__ == "__main__":
    URL = "https://www.carsales.com.au/cars/results/?q=%28And.Service.CARSALES._.Seats.range%287..%29._.%28C.State.Victoria._.Region.Melbourne.%29_.Doors.5._.SiloType.Dealer%20used%20cars._.Year.range%282010..2012%29._.%28C.Make.Toyota._.Model.Kluger.%29%29&sortby=TopDeal&limit=50"
    # URL = "https://www.carsales.com.au/cars/dealer/private/demo/toyota/kluger/grande-badge/gsu55r-series/victoria-state/3008-10km-postcode/automatic-transmission/?WT.z_srchsrcx=makemodel"

    # fake request as a browser to avoid block
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(URL, headers=headers)

    df = parsehtmltoDataFrame(response.text)
    df.to_csv('usercard_' + '.csv')
    print(df)

    print(df.info)
