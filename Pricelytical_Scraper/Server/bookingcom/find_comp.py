from Server.bookingcom.coord_calc import box_handle
from geopy.distance import great_circle
import requests
import pandas as pd
import sqlite3
import traceback
from datetime import date
import math
import json



def find_competitors(hotel_url, checkInDate, checkOutDate, adults, children='0',query_filters=None, hotels_names=None,hotels_number=None,hotels_type='all',perimeter=None):

    hotel_data = pd.DataFrame(
        columns=['Hotel_id', 'Hotel_name', 'Locality', 'Acomodation_type', 'Adults','Children', 'Star_rating', 'Distance_from_Hotel',
                 'Hotel_coordinates', 'map_filter', 'Price',
                 'Customer_rating', 'checkInDate', 'checkOutDate', 'ADP', 'URL'])

    search_word = 'highlighted_blocks='
    substr_index = hotel_url.find(search_word)
    dest_id = hotel_url[substr_index + len(search_word):hotel_url.find("_", substr_index + len(search_word)) - 2]
    limit = '500'
    box_len_fromhotel = 0.1  # km

    checkinsplit = checkInDate.split('-')
    checkoutsplit = checkOutDate.split('-')
    days = abs((date(int(checkinsplit[0]), int(checkinsplit[1]), int(checkinsplit[2])) - date(int(checkoutsplit[0]),
                                                                                          int(checkoutsplit[1]),
                                                                                          int(checkoutsplit[
                                                                                                  2]))).days)
    room_layout=['A']
    for ad in range(1,int(adults)):
        room_layout.append(',A')
    for ch in range(int(children)):
        room_layout.append(',10')
    room_layout=''.join(room_layout)
    print(room_layout)
    room_str = ';room1='+ room_layout + ';'
    print(room_str)

    on_map_url = "https://www.booking.com/hotels_onmap_detail?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQi4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4AoqRsfQFwAIB;sid=10f6af21edae8f956365c1587a686c93;srpvid=d5c999e3242e004c&amp;;lang=en;act=d-hotel;detail=0;currency=USD;av=1;c=1;stype=1;cc1=gr;aid=304142;dest_id=-820164;dest_type=city;img_size=90;localize_format=1;gfa=1%20;rr=1%20;rp=1;checkin="+checkInDate+";checkout="+checkOutDate+";g=1" + room_str + "stl=1;fcob=1;v=1;rpr=1;nn=1;pd=1;ugr=1;st=1;blsd=1;bpl=1;deals=1;pt=1;nvrs=1;shws=1;srocc=1&hotel_id=" + dest_id + "&_=1586296424779"
    params = {"hotel_id": dest_id}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0", }
    resp = requests.get(url=on_map_url, params=params, headers=headers)
    print('resp came')
    data_target_hotel = resp.json()  # Check the JSON Response Content documentation below
    hotel_coordinates = (
        data_target_hotel["b_hotels"][dest_id]["b_latitude"], data_target_hotel["b_hotels"][dest_id]["b_longitude"])


    box_left_init = box_handle(hotel_coordinates[0], hotel_coordinates[1], (-1, -1), box_len_fromhotel)
    box_right_init = box_handle(hotel_coordinates[0], hotel_coordinates[1], (1, 1), box_len_fromhotel)

    tot_flag=True

    init_filter=0
    if query_filters is not None:
        hotel_query="Star_rating >= "+query_filters["minStars"]+" and Star_rating <= "+query_filters["maxStars"]+" and Customer_rating >= "+query_filters["minCustomRating"]+" and Customer_rating <= "+query_filters["maxCustomRating"]+" and Acomodation_type=='hotel' and Distance_from_Hotel>0"
        room_query="Star_rating >= "+query_filters["minStars"]+" and Star_rating <= "+query_filters["maxStars"]+" and Customer_rating >= "+query_filters["minCustomRating"]+" and Customer_rating <= "+query_filters["maxCustomRating"]+" and Acomodation_type=='room' and Distance_from_Hotel>0"

    while init_filter==0 or tot_flag :
        for x in range(-init_filter, init_filter + 1):
            for y in range(-init_filter, init_filter + 1,init_filter*2 if abs(x)<init_filter else 1):
                box_left = box_handle(box_left_init[0], box_left_init[1], (x, y), box_len_fromhotel * 2)
                box_right = box_handle(box_right_init[0], box_right_init[1], (x, y), box_len_fromhotel * 2)
                print(x, y)
                url = "https://www.booking.com/markers_on_map?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQi4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4AvTdrfQFwAIB;sid=10f6af21edae8f956365c1587a686c93;srpvid=0c58807151590007&;aid=304142;dest_id=" + dest_id + ";dest_type=hotel;sr_id=;ref=hotel;limit=" + limit + ";stype=1;lang=en-gb;ssm=1;checkin=" + checkInDate + ";checkout=" + checkOutDate + ";ngp=1" + room_str + "maps_opened=1;sr_countrycode=gr;sr_lat=;sr_long=;dbc=1;tclm=10%20;sod=1%20;sfd=1%20;scc=1%20;somp=1%20;hr=3%20;shp=1;tp=1;spr=1;currency=EUR;srh=;cs=;shws=1%20;huks=1;mdimb=1%20;tp=1%20;img_size=1000x1000%20;avl=1%20;nor=1%20;spc=1%20;rmd=1%20;slpnd=1%20;sbr=1;BBOX=" + str(
                    box_left[1]) + "," + str(box_left[0]) + "," + str(box_right[1]) + "," + str(
                    box_right[0]) + "&_=1586269975549"
                url = url.encode('utf-8')
                params = {
                    # "label":"gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQi4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4AvTdrfQFwAIB;sid=10f6af21edae8f956365c1587a686c93;srpvid=0c58807151590007",
                    # ";aid":"304142;dest_id=241553;dest_type=hotel;sr_id=;ref=hotel;limit="+limit+";stype=1;lang=el;ssm=1;checkin=2020-09-01;checkout=2020-09-11;ngp=1;room1=A,A;maps_opened=1;sr_countrycode=gr;sr_lat=;sr_long=;dbc=1;tclm=10 ;sod=1 ;sfd=1 ;scc=1 ;somp=1 ;hr=3 ;shp=1;tp=1;spr=1;currency=EUR;srh=;cs=;shws=1 ;huks=1;mdimb=1 ;tp=1 ;img_size=270x200 ;avl=1 ;nor=1 ;spc=1 ;rmd=1 ;slpnd=1 ;sbr=1;BBOX=23.647063698196558,35.335565553222764,24.22878978079721,35.683896530021634",
                    # "_":"1586198342694"
                }

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
                }

                resp = requests.get(url=url, params=params, headers=headers)
                data = resp.json()  # Check the JSON Response Content documentation below
                hotel_list = data['b_hotels']
                if init_filter>0:
                    hotel_list = hotel_list[1:]

                for hotel in hotel_list:
                    latitude = float(hotel['b_latitude'])
                    longitude = float(hotel['b_longitude'])
                    targetcoord = (latitude, longitude)
                    customer_rating = hotel['b_review_score']
                    if customer_rating == None:
                        customer_rating = 0
                    stars = hotel['b_class']
                    acom_type = 'hotel'
                    if stars == 0:
                        if 'b_bh_quality_class' in hotel:
                            stars = hotel['b_bh_quality_class']
                            acom_type = 'room'


                    hotel_data = hotel_data.append(
                        {
                            'Hotel_id': hotel['b_id'],
                            'Hotel_name': hotel['b_hotel_title'],
                            'Locality' : data['b_free_districts'][0]['name'].split(' ')[0]+',Greece',
                            'Acomodation_type': acom_type,
                            'Adults':adults,
                            'Children': children,
                            'Star_rating': stars,
                            'Distance_from_Hotel': great_circle(targetcoord, hotel_coordinates).km,
                            'Hotel_coordinates': str(targetcoord[0]) + ',' + str(targetcoord[1]),
                            'map_filter':   str(x)+','+str(y),
                            'Price': int(''.join(hotel['b_u_total_price'][2:].split(','))) if 'b_u_total_price' in hotel else 0,
                            'Customer_rating': float(customer_rating),
                            'checkInDate': checkInDate,
                            'checkOutDate': checkOutDate,
                            'ADP': int(''.join(hotel['b_u_total_price'][2:].split(','))) / days if 'b_u_total_price' in hotel else 0,
                            'URL': 'https://www.booking.com/'+ hotel['b_url']
                        },
                        ignore_index=True)
        init_filter += 1
        if hotels_number is not None:
            if hotels_type=='all':
                tot_hotel_flag = len(hotel_data.query(hotel_query).index) < hotels_number + 1
                tot_room_flag = len(hotel_data.query(room_query).index) < hotels_number+1
                tot_flag= tot_hotel_flag or tot_room_flag
            elif hotels_type=='hotel':
                tot_hotel_flag = len(hotel_data.query(hotel_query).index) < hotels_number + 1
                tot_flag = tot_hotel_flag
            elif hotels_type == 'room':
                tot_room_flag = len(hotel_data.query(room_query).index) < hotels_number + 1
                tot_flag = tot_room_flag
        elif hotels_names is not None:
            tot_hotel_names = len(hotel_data[hotel_data['Hotel_name'].isin(hotels_names)].index) < len(hotels_names)
            tot_flag = tot_hotel_names
        elif perimeter is not None:
            radius = (init_filter-1)*(box_len_fromhotel * 1e3 * 2)
            tot_flag= radius < perimeter*1e3


   
    dftocsv=pd.DataFrame(columns=hotel_data.columns)
    
    if hotels_number is not None:
        if hotels_type=='all':
            dftocsv=dftocsv.append(hotel_data.query(hotel_query).sort_values(by=['Distance_from_Hotel','Customer_rating']).head(hotels_number))
            dftocsv=dftocsv.append(hotel_data.query(room_query).sort_values(by=['Distance_from_Hotel','Customer_rating']).head(hotels_number))
        elif hotels_type=='hotel':
            dftocsv = dftocsv.append(hotel_data.query(hotel_query).sort_values(by=['Distance_from_Hotel', 'Customer_rating']).head(hotels_number))
        elif hotels_type=='room':
            dftocsv = dftocsv.append(hotel_data.query(room_query).sort_values(by=['Distance_from_Hotel', 'Customer_rating']).head(hotels_number))
    elif hotels_names is not None:
        dftocsv=dftocsv.append(hotel_data[hotel_data['Hotel_name'].isin(hotels_names)])
    elif perimeter is not None:
        dftocsv=dftocsv.append(hotel_data.sort_values(by=['Distance_from_Hotel','Customer_rating']))

    dftocsv.to_excel(r'.\competitors.xlsx', index=False, header=True)
    return dftocsv
