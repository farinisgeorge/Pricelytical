from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep,time
from bs4 import BeautifulSoup
import re



def tripcom_hotel(browser,hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children):

    ages='0'
    if int(children)>0:
        ages = '10'
        if int(children)>1:
            for i in range(int(children)-1):
                ages = ages+',10'



    url='https://us.trip.com/?locale=en_us&curr=EUR'
    action=ActionChains(browser)
    browser.get(url)
    destinationField=browser.find_element_by_xpath('//input[contains(@id,"hotels-destination")]')
    searchbutton=browser.find_element_by_class_name('search-btn-wrap')


    if destinationField and searchbutton:
        destinationField.send_keys(Keys.CONTROL,"a")
        destinationField.send_keys(Keys.DELETE)
        destinationField.send_keys(destinationHotel)
        sleep(2)
        hotel_list=browser.find_elements_by_class_name("associative-item")
        for element in hotel_list:
            if element.find_element_by_xpath('.//span[contains(@class,"type")]').text == "Hotel":
                action.move_to_element(element).click().perform()
                break
        searchbutton = browser.find_element_by_class_name('search-btn-wrap').click()

    
    hotel_link=browser.current_url
    search_link_splited=hotel_link.split('=')
    search_link_splited[3] = checkInDate +'&checkout'
    search_link_splited[4] = checkOutDate + '&optionId'
    search_link_splited[9] = rooms + '&adult'
    search_link_splited[10] = adults + '&children'
    search_link_splited[11] = children + '&ages'
    search_link_splited[12] = ages + '&searchBoxArg'
    newlink='='.join(search_link_splited)
    # browser.delete_cookie('_abtest_userid')
    # browser.add_cookie({'name' : '_abtest_userid' ,'value' : '2bfe54c8-317d-461f-b1bb-9e7cb9b49743'})
    browser.get(newlink)
    sleep(4)

    soup = BeautifulSoup(browser.page_source, 'lxml')
    hotel_containers=soup.find_all('div', class_='with-decorator-wrap')

    target_hotel_name=None
    price_after_tax=None
    for hotel in hotel_containers:
        if re.sub(r'[^\w]', '',hotel.find('span', class_='name font-bold').text.lower())==re.sub(r'[^\w]', '',hotelname.lower()):
            target_hotel_name=hotel.find('span', class_='name font-bold').text.lower()
            price_boarder=hotel.find('div', class_='list-card-price')
            price_after_tax=price_boarder.find('p', class_='tax').text
            break
    browser.delete_all_cookies()
    finalprice=None    
    if target_hotel_name==None:
        finalprice='Not Found'
    elif price_after_tax=='':
        finalprice='Sold Out'
    else:
        finalprice=price_after_tax.replace('€','').split(' ')[2]
    return finalprice

