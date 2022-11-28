from bs4 import BeautifulSoup
import requests
from currency_converter import CurrencyConverter
from datetime import date
import re



def ebookers_hotel(hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children):
    childstr='0'
    if int(children)>0:
        childstr = '1_10'
        if int(children)>1:
            for i in range(int(children)-1):
                childstr = childstr+',1_10'

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
        "Accept-Language": "en-gb ",
        "Accept-Encoding" : "br, gzip, deflate",
        "Accept" : "test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer" : "http://www.google.com/",
    }
    url="https://www.ebookers.com/Hotel-Search?destination="+'+'.join(destinationHotel.split(' '))+"&hotelName="+'+'.join(destinationHotel.split(' '))+"&startDate="+checkInDate+\
        "&endDate="+checkOutDate+"&d1="+checkInDate+"&d2="+checkOutDate+"&rooms="+rooms+"&adults="+adults+"&children="+childstr

    response=requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,'html.parser')
    containers = soup.find_all(class_="uitk-card-content uitk-grid uitk-cell all-y-padding-three all-x-padding-three listing-content")
    sitehotelname=None
    price=None
    for container in containers:
        if re.sub(r'[^\w]', '',container.find("h3",{"data-stid":"content-hotel-title"}).text.lower())==re.sub(r'[^\w]', '',hotelname.lower()):
            targethotel=container
            sitehotelname=targethotel.find("h3",{"data-stid":"content-hotel-title"}).text.lower()
            price=targethotel.find("span",{"data-stid":"content-hotel-lead-price"}).text if targethotel.find("span",{"data-stid":"content-hotel-lead-price"}) is not None else None
            extramessages = targethotel.find("div", {"data-stid": "supporting-messages-0"}).text if targethotel.find("div", {"data-stid": "supporting-messages-0"}) is not None else 'No Message'

    #Mporo na parw kai asteria kai bathmologia pelaton
    finalprice=None
    conv=CurrencyConverter()

    checkin_split=[int(x) for x in checkInDate.split('-')]
    checkout_split=[int(x) for x in checkOutDate.split('-')]
    st_date=date(checkin_split[0],checkin_split[1],checkin_split[2])
    end_date=date(checkout_split[0],checkout_split[1],checkout_split[2])
    delta=end_date-st_date

    if sitehotelname and price:
        price=price.replace('£','')
        price=price.replace(',','')
        finalprice=str(conv.convert(int(price)/delta.days,'GBP','EUR'))
    elif price=='':
        finalprice='Sold Out'
    else:
        finalprice='Not Found'
    return finalprice