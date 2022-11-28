import requests
from coord_calc import box_handle
from geopy.distance import great_circle
import math
from datetime import date


def booking_scrape_perimeter(hotel_url, checkInDate, checkOutDate, room_layout, df):
    search_word = 'highlighted_blocks='
    substr_index = hotel_url.find(search_word)
    dest_id = hotel_url[substr_index + len(search_word):hotel_url.find("_", substr_index + len(search_word)) - 2]
    # Na parw to url kai na to spasw gia to request gia tis sintetagmenes#
    # dest_id="190238"
    # hotel_coordinates=(40.638950,22.940910)       #(lat,long)
    limit = '500'
    box_len_fromhotel = 0.5  # km
    perimeter = 3  # km

    checkinsplit=checkInDate.split('-')
    checkoutsplit=checkOutDate.split('-')
    days=(date(int(checkinsplit[0]),int(checkinsplit[1]),int(checkinsplit[2])) - date(int(checkoutsplit[0]),int(checkoutsplit[1]),int(checkoutsplit[2]))).days

    on_map_url = "https://www.booking.com/hotels_onmap_detail?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQi4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4AoqRsfQFwAIB;sid=10f6af21edae8f956365c1587a686c93;srpvid=d5c999e3242e004c&amp;;lang=el;act=d-hotel;detail=0;currency=USD;av=1;c=1;stype=1;cc1=gr;aid=304142;dest_id=-820164;dest_type=city;img_size=90;localize_format=1;gfa=1%20;rr=1%20;rp=1;checkin=2020-09-01;checkout=2020-09-11;g=1;room1=A,A,4,5,6;stl=1;fcob=1;v=1;rpr=1;nn=1;pd=1;ugr=1;st=1;blsd=1;bpl=1;deals=1;pt=1;nvrs=1;shws=1;srocc=1&hotel_id=" + dest_id + "&_=1586296424779"
    params = {"hotel_id": dest_id}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0", }
    resp = requests.get(url=on_map_url, params=params, headers=headers)
    print('resp came')
    data_target_hotel = resp.json()  # Check the JSON Response Content documentation below
    hotel_coordinates = (
    data_target_hotel["b_hotels"][dest_id]["b_latitude"], data_target_hotel["b_hotels"][dest_id]["b_longitude"])

    room_str = ';'
    for room in range(len(room_layout)):
        room_str = room_str + 'room' + str(room + 1) + '=' + room_layout[room] + ';'

    box_left_init = box_handle(hotel_coordinates[0], hotel_coordinates[1], (-1, -1), box_len_fromhotel)
    box_right_init = box_handle(hotel_coordinates[0], hotel_coordinates[1], (1, 1), box_len_fromhotel)
    radius = math.ceil(((perimeter * 1000) - box_len_fromhotel * 1000) / (box_len_fromhotel * 1000 * 2))

    for x in range(-radius, radius + 1):
        for y in range(-radius, radius + 1):
            box_left = box_handle(box_left_init[0], box_left_init[1], (x, y), box_len_fromhotel * 2)
            box_right = box_handle(box_right_init[0], box_right_init[1], (x, y), box_len_fromhotel * 2)
            print(x, y)
            url = "https://www.booking.com/markers_on_map?aid=304142;label=gen173nr-1FCAEoggI46AdIM1gEaFyIAQGYAQi4ARfIAQ_YAQHoAQH4AQuIAgGoAgO4AvTdrfQFwAIB;sid=10f6af21edae8f956365c1587a686c93;srpvid=0c58807151590007&;aid=304142;dest_id=" + dest_id + ";dest_type=hotel;sr_id=;ref=hotel;limit=" + limit + ";stype=1;lang=el;ssm=1;checkin=" + checkInDate + ";checkout=" + checkOutDate + ";ngp=1" + room_str + "maps_opened=1;sr_countrycode=gr;sr_lat=;sr_long=;dbc=1;tclm=10%20;sod=1%20;sfd=1%20;scc=1%20;somp=1%20;hr=3%20;shp=1;tp=1;spr=1;currency=EUR;srh=;cs=;shws=1%20;huks=1;mdimb=1%20;tp=1%20;img_size=1000x1000%20;avl=1%20;nor=1%20;spc=1%20;rmd=1%20;slpnd=1%20;sbr=1;BBOX=" + str(
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
            if x > -radius or y > -radius:
                hotel_list = hotel_list[1:]
            for hotel in hotel_list:
                latitude = float(hotel['b_latitude'])
                longitude = float(hotel['b_longitude'])
                targetcoord = (latitude, longitude)
                customer_rating = hotel['b_review_score']
                if customer_rating == None:
                    customer_rating = 0
                stars=hotel['b_class']
                acom_type='hotel'
                if stars==0:
                    if 'b_bh_quality_class' in hotel:
                        stars=hotel['b_bh_quality_class']
                        acom_type = 'room'
                if 'b_u_total_price' in hotel:
                    df = df.append(
                        {
                            'Hotel_id': hotel['b_id'],
                            'Hotel_name': hotel['b_hotel_title'],
                            'Acomodation_type': acom_type,
                            'Star_rating': stars,
                            'Distance_from_Hotel': great_circle(targetcoord, hotel_coordinates).km,
                            'Hotel_coordinates': str(targetcoord[0]) + ',' + str(targetcoord[1]),
                            'Price': int(''.join(hotel['b_u_total_price'][2:].split('.'))),
                            'Customer_rating': float(customer_rating),
                            'checkInDate': checkInDate,
                            'checkOutDate': checkOutDate,
                            'ADP': int(''.join(hotel['b_u_total_price'][2:].split('.')))/days,
                        },
                        ignore_index=True)
    return df







