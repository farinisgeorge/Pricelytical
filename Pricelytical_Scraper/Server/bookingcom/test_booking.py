import find_comp

hotel_url="https://www.booking.com/hotel/gr/samaria.en-gb.html?label=gen173nr-1DCAEoggI46AdIM1gEaFyIAQGYAQm4ARfIAQ_YAQPoAQGIAgGoAgO4AsLb7vYFwAIB0gIkM2E5OGVmZGQtYmQ2Mi00NjdjLTgwZGEtNWE2M2E2NmMyZGUy2AIE4AIB;all_sr_blocks=24155302_239270889_2_1_0;checkin=2020-07-08;checkout=2020-07-09;dest_id=-820164;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=1;highlighted_blocks=24155302_239270889_2_1_0;hpos=1;no_rooms=1;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=24155302_239270889_2_1_0__19300;srepoch=1591455188;srpvid=72bc68aa90e600e4;type=total;ucfs=1&#map_closed"
checkInDate = "2020-10-01"  # Format %d/%m/%Y
checkOutDate = "2020-10-11"  # Format %d/%m/%Y
adults='02'
children='1'

find_comp.find_competitors(hotel_url,checkInDate,checkOutDate,adults,children=children,hotels_number=4,hotels_type='hotel')


