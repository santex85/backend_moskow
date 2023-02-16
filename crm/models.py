from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Position(models.Model):
    name = models.CharField("Должность", max_length=256)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Employee(User):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.position}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Group(models.Model):
    CHOICE_STATUS = [("preregister", "Предварительная регистрация"), ("register", "Регистрация"),
                     ("inhotel", "В отеле"), ("finish", "Завершен")]
    name = models.CharField("Название группы", max_length=256)
    count_guests = models.IntegerField("Количество гостей", default=1)
    tag = models.CharField("Тег группы", max_length=25, unique=True)
    group_organizer = models.CharField("Имя инструктора", max_length=256)
    date_checkin = models.DateField("Дата заселения")
    date_checkout = models.DateField("Дата выселения")
    hotel = models.ForeignKey("Hotel", verbose_name="Отель", on_delete=models.CASCADE)
    status = models.CharField("Статус группы", choices=CHOICE_STATUS, max_length=30,
                              default="Предварительная регистрация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Guest(models.Model):
    name = models.CharField("Имя", max_length=256)
    surname = models.CharField("Фамилия", max_length=256)
    telephone = models.CharField("Телефон", max_length=256)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_checkin = models.DateField("Дата заселения", blank=True)
    date_checkout = models.DateField("Дата выселения", blank=True)

    def __str__(self):
        return f"{self.name}, {self.surname}"

    class Meta:
        verbose_name = "Гость"
        verbose_name_plural = "Гости"


class Hotel(models.Model):
    name = models.CharField("Имя отеля", max_length=256)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"


class Room(models.Model):
    CHOICE = [("full", "Полный"), ("partially", "Частично"), ("empty", "Пустой"), ("over", "Переполненный")]
    number = models.IntegerField("Номер", default=100)
    name = models.CharField("Название номера", max_length=256, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    capacity = models.IntegerField("Количество мест", default=2)
    over_booking = models.IntegerField("Дополнительные места в номер", default=1)
    price = models.IntegerField("Цена", default=0)
    fullness = models.CharField("Статус", choices=CHOICE, max_length=30, default="empty")
    number_guests = models.IntegerField("Количество гостей", default=0)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"


class Goods(models.Model):
    CHOICE = {"volume": "л.", "weight": "кг.", 'quantity': 'шт.'}
    name = models.CharField("Название товара", unique=True, max_length=250)
    count = models.FloatField("Объем/количество в единице")
    unit = models.CharField("Единица измерения", choices=CHOICE.items(), max_length=256, default="weight")
    price = models.FloatField("Стоимость за единицу")
    how_many_unit = models.IntegerField("Количество единиц", default=1)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Товары"
        verbose_name_plural = "Товары"


class Groceries(Goods):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Household(Goods):
    class Meta:
        verbose_name = "Хозтовар"
        verbose_name_plural = "Хозтовары"


class BookingServices(models.Model):
    name = models.CharField("Название", max_length=256)
    start_time_booking = models.DateTimeField()
    finish_time_booking = models.DateTimeField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"


class YogaHall(BookingServices):
    class Meta:
        verbose_name = "Йога хол"
        verbose_name_plural = "Йога холы"


class Sauna(BookingServices):
    class Meta:
        verbose_name = "Сауна"
        verbose_name_plural = "Сауны"


class Service(models.Model):
    name = models.CharField("Название услуги", max_length=256)
    description = models.TextField("Описание услуги", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Cashier(models.Model):
    incomes = models.IntegerField("Входящие средства")
    outcomes = models.IntegerField("Расходы")
    datetime = models.DateTimeField("Дата и время операции", auto_now=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    services = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.services}, {self.guest.name}"

    class Meta:
        verbose_name = "Касса"
