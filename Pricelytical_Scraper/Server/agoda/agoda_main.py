from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep,time
import re
from datetime import date




def agoda_hotel(browser,hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children):
    childages=''
    traveler_type='travellerType=1'
    if int(children)>0:
        traveler_type='travellerType=2'
        childages = 'childages=10'
        if int(children)>1:
            for i in range(int(children)-1):
                childages = childages+'%2C10'


    url='https://www.agoda.com'
    action=ActionChains(browser)
    browser.get(url)


    checkin_split=[int(x) for x in checkInDate.split('-')]
    checkout_split=[int(x) for x in checkOutDate.split('-')]
    st_date=date(checkin_split[0],checkin_split[1],checkin_split[2])
    end_date=date(checkout_split[0],checkout_split[1],checkout_split[2])
    delta=end_date-st_date

    destinationField=browser.find_element_by_class_name('SearchBoxTextEditor.SearchBoxTextEditor--autocomplete')
    searchbutton=browser.find_element_by_class_name('btn.Searchbox__searchButton.Searchbox__searchButton--active')

    if destinationField and searchbutton:
        destinationField.clear()
        destinationField.send_keys(destinationHotel)
        sleep(3)
        destinationField.send_keys(Keys.ENTER)
        randomspot=browser.find_element_by_class_name('IconBox.IconBox--checkIn.IconBox--focused')
        sleep(2)
        action.move_to_element(randomspot).click().perform()
        sleep(1)
        searchbutton.click()

    sleep(4)
    hotel_link=browser.current_url
    price=None
    hotel_name=None
    pagecheck=browser.find_elements_by_class_name('HeaderCerebrum__Name')
    hotel_results=browser.find_elements_by_class_name('property-card-content')
    if len(pagecheck)>0:
        search_link=hotel_link.split('&')
        search_link[16]='checkIn=' + checkInDate
        search_link[17]='checkOut=' + checkOutDate
        search_link[18]='rooms=' + rooms
        search_link[19]='adults=' +adults
        search_link[20]='childs=' + children
        search_link[21]= childages
        search_link[23]='los=' + str(delta.days)
        
        search_link[26]= traveler_type
        
        search_link='&'.join(search_link)
        browser.get(search_link)

        
        search_hotel_name=browser.find_element_by_xpath('.//h1[contains(@class,"HeaderCerebrum__Name")]').text.lower()
        if re.sub(r'[^\w]', '',search_hotel_name.lower())==re.sub(r'[^\w]', '',hotelname.lower()):
            hotel_name=search_hotel_name
            prices=browser.find_elements_by_xpath('.//span[contains(@class,"PriceRibbon__Price")]')
            if len(prices)>0:
                price=prices[0].text
                

    elif len(hotel_results)>0:

        
        search_link=hotel_link.split('&')
        search_link[20]='checkIn=' + checkInDate
        search_link[21]='checkOut=' + checkOutDate
        search_link[22]='rooms=' + rooms
        search_link[23]='adults=' +adults
        search_link[24]='children=' + children
        search_link[25]= childages
        search_link[28]= traveler_type
        search_link.append('sort=personalize')
        search_link='&'.join(search_link)
        browser.get(search_link)

        hotel_results=browser.find_elements_by_class_name('property-card-content')
        
        for hotel in hotel_results:
            search_hotel_name=hotel.find_element_by_xpath('.//h3[contains(@class,"InfoBox__HotelTitle")]').text.lower()
            if re.sub(r'[^\w]', '',search_hotel_name.lower())==re.sub(r'[^\w]', '',hotelname.lower()):
                hotel_name=search_hotel_name
                price=hotel.find_element_by_xpath('.//div[contains(@class,"price-box__price__final")]').text
                break
    
    finalprice=None
    if hotel_name==None:
        finalprice='Not Found'
    elif price==None or price=='':
        finalprice='Sold Out'
    else:
        finalprice=price.replace('€','')
    return finalprice