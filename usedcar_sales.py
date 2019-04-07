import datetime
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup


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

    pricetypes = soup.find_all('div', class_='price-desc')
    # get vehicle prices type
    pricetypelist = [a.text for a in pricetypes]

    cardata = {}
    cardata['cartitle'] = vehtitle
    cardata['kms'] = odometers
    cardata['bodytype'] = bodytype
    cardata['engine'] = engine
    cardata['transmission'] = transmission
    cardata['price'] = pricelist
    cardata['price_type'] = pricetypelist
    cardata['year'] = [(int(a.lstrip().split(" ")[0])-2011)*8 for a in vehtitle]
    return pd.DataFrame(cardata)


# make chart in excel workbook
# def makechart(wbname: str):
#     wb = xw.Book(wbname)
#     ws = wb.sheets["Sheet1"]
#     rg = ws.cells[1, 1]
#     # rg.value = "hello"
#
#     if ws.charts.count > 0:
#         ws.charts.clear()
#
#     cht = ws.charts.add()
#     cht.name = 'chart 1'
#     cht.title = 'demo chart'
#     cht.set_source_data(rg.expand())
#     cht.chart_type = 'scatter'      # chart type is not correct
#
#     wb.close()


def makescatterplot(x, y, xtitle, ytitle, plottitle, figsize, fname="new", markersize=None):
    '''
    Make scatter plot with matplot and save as user specified name
    :param x:
    :param y:
    :param xtitle:
    :param ytitle:
    :param plottitle:
    :param figsize:
    :return:
    '''
    matplotlib.use("Agg")
    fig, ax = plt.subplots()
    if markersize:
        ax.scatter(x, y, s=markersize)
    else:
        ax.scatter(x, y)

    ax.set(xlabel=xtitle,
           ylabel=ytitle,
           title=plottitle)
    ax.grid()

    # set font size
    ax.xaxis.label.set_fontsize(10)
    ax.yaxis.label.set_fontsize(10)
    ax.title.set_fontsize(12)

    for tick in ax.xaxis.get_minor_ticks():
        tick.label.set_fontsize(8)

    for tick in ax.yaxis.get_minor_ticks():
        tick.label.set_fontsize(8)

    fig.savefig(fname, dpi=figsize)


def cleardataframe(mydf):
    mydf.price = mydf.price.str.lstrip()
    mydf.price = mydf.price.str.rstrip()
    mydf.price = mydf.price.str.replace('$', '')
    mydf.price = mydf.price.str.replace('*', '')
    mydf.price = mydf.price.str.replace(',', '')
    mydf.price = mydf.price.astype(float)
    mydf.kms = mydf.kms.astype(float)
    mydf.year = mydf.year.astype(float)
    return mydf

'''
TODO:
1. Use marker size/color to indicate year or other property

'''
if __name__ == "__main__":
    starttime = datetime.datetime.now()
    # URL = "https://www.carsales.com.au/cars/results/?q=%28And.Service.CARSALES._.Seats.range%287..%29._.%28C.State.Victoria._.Region.Melbourne.%29_.Doors.5._.SiloType.Dealer%20used%20cars._.Year.range%282010..2012%29._.%28C.Make.Toyota._.Model.Kluger.%29%29&sortby=TopDeal&limit=50"
    # URL = "https://www.carsales.com.au/cars/dealer/private/demo/toyota/kluger/grande-badge/gsu55r-series/victoria-state/3008-10km-postcode/automatic-transmission/?WT.z_srchsrcx=makemodel"

    # fake request as a browser to avoid block
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    comment = "kluger"
    url_kluger = "https://www.carsales.com.au/cars/results/?sortby=TopDeal&limit=30&q=(And.Service.CARSALES._.(C.Make.Toyota._.Model.Kluger.)_.(Or.SiloType.Dealer+used+cars._.SiloType.Private+seller+cars._.SiloType.Demo+and+near+new+cars.)_.(C.State.Victoria._.Region.Melbourne.)_.GenericGearType.Automatic._.FuelType.Petrol+-+Unleaded+ULP._.BodyStyle.SUV._.Price.range(..25000)._.Year.range(2012..2016).)"
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    response = requests.get(url_kluger, headers=headers)

    if response.status_code == 200:
        df = parsehtmltoDataFrame(response.text)
        df = cleardataframe(df)

        print(df.year)

        filename = input("please key in file name: ")
        # filename = "first"
        makescatterplot(df['price'],
                        df['kms'],
                        'Price in AUD',
                        'Kms',
                        'Car mileage and price scatter ' + comment,
                        500,
                        filename,
                        markersize=list(df.year))

        stoptime = datetime.datetime.now()
        print('plot finished in {0} seconds'.format(stoptime - starttime))
    else:
        print("fail to get webpage")

    '''
    # makechart('demo.xlsx')

    # URL = "https://www.carsales.com.au/cars/results/?q=%28And.Service.CARSALES._.Seats.range%287..%29._.%28C.State.Victoria._.Region.Melbourne.%29_.Doors.5._.SiloType.Dealer%20used%20cars._.Year.range%282010..2012%29._.%28C.Make.Toyota._.Model.Kluger.%29%29&sortby=TopDeal&limit=50"
    # URL = "https://www.carsales.com.au/cars/dealer/private/demo/toyota/kluger/grande-badge/gsu55r-series/victoria-state/3008-10km-postcode/automatic-transmission/?WT.z_srchsrcx=makemodel"

    # fake request as a browser to avoid block
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # response = requests.get(URL, headers=headers)
    #
    # df = parsehtmltoDataFrame(response.text)
    # df.to_csv('usercard_' + str(datetime.date.today()) + '.csv')
    # wbname = 'usedcar_' + str(datetime.date.today()) + '.xlsx'
    # df.to_excel(wbname)
    # print(df)
    # print(df.info)
    # where xlwings come in to plot scatter plot of mileage and price
    '''
