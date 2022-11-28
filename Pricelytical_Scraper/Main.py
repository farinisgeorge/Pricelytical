from Server.Webdriver_manipulation import webdriver_spawn, webdriver_kill,set_options
from time import time, sleep
from Server.agoda import agoda_main
from Server.bookingcom import find_comp
from Server.ebookers import ebookers_main
from Server.Expedia import expedia_mainpage
from Server.Hotelscom import hotelscom_mainpage
from Server.tripcom import tripcom_mainpage
from Server.Zenhotels import zenhotels_mainpage
from Server.trivago import trivago_hotel_search
import pandas as pd

#########  inputs  ############
hotel_url="https://www.booking.com/hotel/gr/samaria.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaFyIAQGYAQm4ARfIAQ_YAQPoAQGIAgGoAgO4AsLb7vYFwAIB0gIkM2E5OGVmZGQtYmQ2Mi00NjdjLTgwZGEtNWE2M2E2NmMyZGUy2AIE4AIB;all_sr_blocks=24155302_239270889_2_1_0;checkin=2020-07-08;checkout=2020-07-09;dest_id=-820164;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=24155302_239270889_2_1_0;hpos=1;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=24155302_239270889_2_1_0__19300;srepoch=1591455188;srpvid=72bc68aa90e600e4;type=total;ucfs=1&#map_closed"
checkInDate = "2020-09-01"  # Format %MM/%DD/%YY
checkOutDate = "2020-09-05"  # Format %MM/%DD/%YY
rooms='1'
adults='02'
children='0'

query_filters={
    "minStars" : "4",
    "maxStars" : "5",
    "minCustomRating" : "8.5",
    "maxCustomRating" : "10",
}
####################

try:
    hotelscom_data= pd.DataFrame(columns=['Hotel_name','Address','Stars','Check_in_Date','Check_out_Date', 'Website', 'Price'])
    browser=webdriver_spawn(1,set_options())
    start_time=time()

    hotels_df=find_comp.find_competitors(hotel_url,checkInDate,checkOutDate,adults, query_filters=query_filters,children=children,hotels_number=10,hotels_type='hotel')

    for _,hotel in hotels_df.iterrows():
        hotelname=hotel['Hotel_name']
        locality=hotel['Locality']
        destinationHotel=hotelname+','+locality
        print(destinationHotel)
        print('==================================================================')

        trivago_prices=trivago_hotel_search.hotel_search(browser,hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children)    #timi ana mera
        agoda_price=agoda_main.agoda_hotel(browser,hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children)               #timi ana mera
        if agoda_price != 'Not Found':
            trivago_prices.update({'Agoda' : agoda_price} )

        ebook_price=ebookers_main.ebookers_hotel(hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children)                 #sinoliki timi
        if ebook_price != 'Not Found':
            trivago_prices.update({'Ebook' : ebook_price} )

        expedia_price=expedia_mainpage.expedia_hotel(hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children)               #sinoliki timi
        if expedia_price != 'Not Found':
            trivago_prices.update({'Expedia' : expedia_price} )

        hotelscom_price=hotelscom_mainpage.hotelscom_hotel(browser,hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children)   #timi ana mera,mporo na parw polles plirofories gia to ksenodoxeio
        if hotelscom_price != 'Not Found':
            trivago_prices.update({'Hotels.com' : hotelscom_price} )

        tripcom_price=tripcom_mainpage.tripcom_hotel(browser,hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children)       #sinoliki timi
        if tripcom_price != 'Not Found':
            trivago_prices.update({'Trip.com' : tripcom_price} )

        zenhotels_price=zenhotels_mainpage.zenhotels_hotel(browser,hotelname,destinationHotel,checkInDate,checkOutDate,rooms,adults,children)   #sinoliki timi
        if zenhotels_price != 'Not Found':
            trivago_prices.update({'ZenHotels.com' : zenhotels_price} )

        if hotel['ADP'] != 0:
            trivago_prices.update({'Booking' : str(hotel['ADP'])} )
        for key, value in trivago_prices.items():
            print(key,' : ',value)
        print('==================================================================')
    

finally:

    end_time=time()
    print(f'Total execution time: {str((end_time-start_time)/60)} mins')
    webdriver_kill(browser,1)

#TODO clear destination fields before writing destination
#TODO periptoseis na mi skaei otan de briskei to ksenodoxeio
#TODO Organosi arxeion san app
#TODO Use hotels dataframe to query and scrape hotels