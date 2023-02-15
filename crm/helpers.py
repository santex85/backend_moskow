from django.db.models import Sum


def change_fullness(room):
    """change status room depending on occupancy"""
    capacity = room.capacity
    number_guests = room.number_guests
    if number_guests >= capacity:
        room.fullness = "full"
    if number_guests < capacity and number_guests != 0:
        room.fullness = "partially"
    if number_guests == 0:
        room.fullness = "empty"
    room.save()


def get_title_object_info(obj):
    """get information about object"""
    rooms = obj.room_set.all()
    rooms_in_hotel = len(rooms)
    number_guest_in_hotel = rooms.aggregate(Sum('number_guests'))['number_guests__sum']
    capacity_in_hotel = rooms.aggregate(Sum('capacity'))['capacity__sum']
    extra_places_in_hotel = rooms.aggregate(Sum('over_booking'))['over_booking__sum']
    free_place_hotel = capacity_in_hotel - number_guest_in_hotel
    potential_places_hotel = extra_places_in_hotel + capacity_in_hotel
    setattr(obj, 'number_guest_in_hotel', number_guest_in_hotel)
    setattr(obj, 'rooms_in_hotel', rooms_in_hotel)
    setattr(obj, 'capacity_in_hotel', capacity_in_hotel)
    setattr(obj, 'extra_places_in_hotel', extra_places_in_hotel)
    setattr(obj, 'free_place_hotel', free_place_hotel)
    setattr(obj, 'potential_places_hotel', potential_places_hotel)
    setattr(obj, 'fullness_hotel', round((number_guest_in_hotel * 100) / capacity_in_hotel))
