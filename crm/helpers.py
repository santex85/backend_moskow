import random
from datetime import datetime, timedelta, date
from typing import List, Tuple

from django.db.models import Sum, Q
from faker import Faker
from crm.models import Hotel, Room, Groceries, Goods, Booking, Guest


def change_fullness(room: Room):
    """
    Функция change_fullness() принимает в качестве аргумента объект класса Room.
    Она определяет степень загруженности комнаты (полная, частично заполненная, пустая) и сохраняет эту информацию в базе данных.
    """
    capacity = room.capacity
    number_guests = room.number_guests
    if number_guests >= capacity:
        room.fullness = "full"
    if number_guests < capacity and number_guests != 0:
        room.fullness = "partially"
    if number_guests == 0:
        room.fullness = "empty"
    room.save()


def get_title_objects_info(date_checkin: date, date_checkout, hotel: Hotel = None) -> List[List[Booking]]:
    """
        Возвращает список списков объектов `Booking` для всех отелей или для указанного отеля `hotel`,
        которые доступны для бронирования в указанный период.

        Если указан конкретный отель, то возвращается список `Booking` для этого отеля.
        Если `hotel` не указан, то возвращается список списков `Booking` для всех отелей.

        :param date_checkin: Объект `date`, представляющий дату заезда.
        :param date_checkout: Объект `date`, представляющий дату выезда.
        :param hotel: Опциональный объект `Hotel`, представляющий искомый отель.
        :return: Список списков объектов `Booking` для всех отелей или для указанного отеля `hotel`.
        """
    rooms = Room.objects.all()
    hotels = Hotel.objects.all()
    objects = []
    if hotel is not None:
        objects = get_booking(hotel, date_checkin, date_checkout, rooms)
    else:
        for hotel in hotels:
            objects.append(get_booking(hotel, date_checkin, date_checkout, rooms))
    return objects


def get_booking(hotel, date_checkin, date_checkout, rooms):
    """
        Вычисляет информацию об заполненности и вместимости для заданного `hotel` в указанный период дат заезда и
        выезда, учитывая доступность `rooms` в отеле в течение этого периода.

        :param hotel: Объект `Hotel`, представляющий искомый отель.
        :param date_checkin: Объект `date`, представляющий дату заезда.
        :param date_checkout: Объект `date`, представляющий дату выезда.
        :param rooms: Список объектов `Room`, представляющих искомые номера.
        :return: Объект `Hotel` с вычисленной информацией о заполненности и вместимости.
        """
    hotel_rooms = rooms.filter(hotel=hotel)
    bookings = Booking.objects.filter(Q(date_checkin__range=(date_checkin, date_checkout)) | Q(
        date_checkout__range=(date_checkin, date_checkout)), room__hotel_id=hotel.id)
    rooms_in_hotel = len(hotel_rooms)
    number_guest_in_hotel = len(bookings.select_related('guest'))
    if not isinstance(number_guest_in_hotel, int):
        number_guest_in_hotel = 0
    capacity_in_hotel = rooms.filter(hotel_id=hotel.id).aggregate(Sum("capacity"))["capacity__sum"]
    extra_places_in_hotel = rooms.aggregate(Sum("over_booking"))["over_booking__sum"]
    free_place_hotel = int(capacity_in_hotel) - int(number_guest_in_hotel)
    potential_places_hotel = extra_places_in_hotel + capacity_in_hotel
    setattr(hotel, "number_guest_in_hotel", number_guest_in_hotel)
    setattr(hotel, "rooms_in_hotel", rooms_in_hotel)
    setattr(hotel, "capacity_in_hotel", capacity_in_hotel)
    setattr(hotel, "extra_places_in_hotel", extra_places_in_hotel)
    setattr(hotel, "free_place_hotel", free_place_hotel)
    setattr(hotel, "potential_places_hotel", potential_places_hotel)
    setattr(hotel, "fullness_hotel", round((number_guest_in_hotel * 100) / capacity_in_hotel))
    return hotel


def get_equivalent_products(product: Groceries, goods: Goods):
    """
        Функция для вычисления суммы товара.

        :param product: Объект товара из модели Goods(Groceries)
        :param goods: Объект модели Goods
        :return: Объект товара с дополнительным полем equivalent (эквивалент)
        """

    equivalent = product.how_many_unit * product.price
    product.unit = goods.CHOICE[product.unit]
    setattr(product, "equivalent", equivalent)
    return product


def get_products(model):
    """
        Получает список объектов модели, переданной в качестве аргумента.

        Для каждого объекта в списке выполняется функция get_equivalent_products,
        которая добавляет в объект поля, связанные с эквивалентными продуктами,
        используя информацию из модели Goods.
        """
    products = model.objects.all()
    for product in products:
        get_equivalent_products(product, Goods)
    return products


def validate_date(request) -> Tuple[datetime, datetime]:
    """
       Проверяет и преобразует даты, полученные из GET-запроса HTTP в Django.
       Если даты не были указаны в запросе, используется текущая дата.

       :param request: Объект `request` HTTP-запроса Django.
       :return: Кортеж из двух объектов `datetime`.
       """
    if request.GET.get("start_date"):
        start_date = datetime.strptime(request.GET.get("start_date"), "%Y-%m-%d")
    else:
        start_date = datetime.today().date()

    if request.GET.get("end_date"):
        end_date = datetime.strptime(request.GET.get("end_date"), "%Y-%m-%d")
    else:
        end_date = datetime.today().date()
    return start_date, end_date


def fake_booking():
    fake = Faker()
    rooms = Room.objects.all()
    guests = Guest.objects.all()

    for _ in range(100):
        checkin_date = fake.date_between(start_date="-1y", end_date="+1y")
        checkout_date = checkin_date + timedelta(days=random.randint(1, 14))
        random_room = random.choice(rooms)
        random_guest = random.choice(guests)

        Booking.objects.create(
            room=random_room,
            guest=random_guest,
            date_checkin=checkin_date,
            date_checkout=checkout_date
        )
