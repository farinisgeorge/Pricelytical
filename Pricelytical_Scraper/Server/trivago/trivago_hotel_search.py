from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep,time
from currency_converter import CurrencyConverter
import re




def hotel_search(browser,hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children):
    prices_dict={}
    roomtype='8'
    childlist=['']
    if int(children)>0:
        roomtype='9'
        childlist.append('aRooms[0][children][0]=10')
        if int(children)>1:
            for i in range(int(children)-1):
                childlist.append('aRooms[0][children]['+str(i+1)+']=10')


    url='https://www.trivago.com/?settingsChanged=currency'
    action=ActionChains(browser)
    browser.get(url)
    sleep(2)
    
    destinationField=browser.find_element_by_xpath('//input[contains(@class,"js-query input querytext")]')
    searchbutton=browser.find_element_by_class_name('btn.btn--primary.btn--regular.search-button.js-search-button')

    if destinationField and searchbutton:
        destinationField.send_keys(Keys.CONTROL,"a")
        destinationField.send_keys(Keys.DELETE)
        sleep(2)
        for key in destinationHotel:
            destinationField.send_keys(key)
        sleep(4)
        action.move_to_element(searchbutton).click().perform()
        sleep(2)

    hotel_link=browser.current_url
    search_link=hotel_link.split('&')
    if len(search_link)>1:              #in case of the no results page (Aelios Design Hotel,Chania ,Greece)
        search_link[0]= 'https://www.trivago.com/?aDateRange[arr]=' + checkInDate
        search_link[1]= 'aDateRange[dep]=' + checkOutDate
        search_link[4]= 'iRoomType=' + roomtype
        search_link[5]= 'aRooms[0][adults]=' + adults
        final_link='&'.join(search_link[0:6]) + '&'.join(childlist) + '&'.join(search_link[6:])
        
        browser.get(final_link)
        hotel_container=browser.find_elements_by_class_name('hotel-item.item-order__list-item.js_co_item')
        action=ActionChains(browser)
        for hotel in hotel_container:
            hotel_name=hotel.find_element_by_xpath('.//span[contains(@class,"item-link name__copytext")]')
            sleep(2)
            if hotel_name.text!='' and hotel_name.text is not None:
                if re.sub(r'[^\w]', '',hotel_name.text.lower())==re.sub(r'[^\w]', '',hotelname.lower()):
                    prices_button=hotel.find_elements_by_xpath('.//div[contains(@class,"accommodation-list__row")]')
                    if len(prices_button)>0:
                        prices_button[0].click()
                    sleep(5)
                    showmore=hotel.find_elements_by_xpath('.//button[contains(@class,"sl-box__expand-btn pointer td-underline--hover")]')
                    if len(showmore)>0:
                        while showmore[0].text=='Show more':
                            showmore[0].click()

                    sites=hotel.find_elements_by_xpath('.//li[contains(@class,"slideout-deals__item slideout-deals__item--grouped")]')
                    for site in sites:
                        site_name=site.find_element_by_xpath('.//img[contains(@class,"slideout-deal__image")]').get_attribute('title')
                        site_price=site.find_element_by_xpath('.//span[contains(@class,"slideout-deal__price")]').text.split('/')[0].split('\n')[0]
                        conv=CurrencyConverter()
                        prices_dict.update({site_name : str(conv.convert(int(site_price.replace('$','')),'USD','EUR'))} )

                    break
    return prices_dict