import django.utils.timezone as timezone
from django.contrib.auth.models import User
from django.db import models


class Hotel(models.Model):
    name = models.CharField("Имя отеля", max_length=256)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"


class Position(models.Model):
    name = models.CharField("Должность", max_length=256)
    description = models.TextField("Описание")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class Employee(User):
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, default=None)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
        return f"{self.name}"

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Guest(models.Model):
    first_name = models.CharField("Имя", max_length=256)
    last_name = models.CharField("Фамилия", max_length=256)
    telephone = models.CharField("Телефон", max_length=512)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, default=None)
    room = models.ForeignKey("Room", on_delete=models.CASCADE)
    in_hotel = models.BooleanField("В отеле", default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Гость"
        verbose_name_plural = "Гости"


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


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    date_checkin = models.DateField("Дата заселения")
    date_checkout = models.DateField("Дата выселения")


class Goods(models.Model):
    CHOICE = {"volume": "л.", "weight": "кг.", 'quantity': 'шт.'}
    name = models.CharField("Название товара", unique=True, max_length=250)
    count = models.FloatField("Объем/количество в единице", default=0)
    unit = models.CharField("Единица измерения", choices=CHOICE.items(), max_length=256, default="weight")
    price = models.FloatField("Стоимость за единицу")
    how_many_unit = models.FloatField("Количество единиц", default=0)

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


class InventoryControl(models.Model):
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    date_update = models.DateTimeField("Дата обновления", auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField("Количество", default=0)

    def __str__(self):
        return f"{self.goods}"

    class Meta:
        verbose_name = "Складской учет"


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


class CategoryIncome(models.Model):
    name = models.CharField("Название категории", max_length=256)
    description = models.TextField("Описание категории", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория прихода"
        verbose_name_plural = "Категории прихода"


class CategoryOutcome(models.Model):
    name = models.CharField("Название категории", max_length=256)
    description = models.TextField("Описание категории", null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Категория расхода"
        verbose_name_plural = "Категории расхода"


class Cashier(models.Model):
    incomes = models.IntegerField("Приход(сумма)", null=True, blank=True)
    outcomes = models.IntegerField("Расходы(сумма)", null=True, blank=True)
    date_create = models.DateTimeField("Дата и время операции", auto_now=True)
    date_service = models.DateField(verbose_name="Дата услуги", default=timezone.now)
    hotel = models.ForeignKey(Hotel, verbose_name="Объект", on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,
                                 verbose_name="Сотрудник",
                                 on_delete=models.CASCADE,
                                 null=True,
                                 blank=True)

    guest = models.ForeignKey(Guest,
                              verbose_name="Гость",
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)

    group = models.ForeignKey(Group,
                              verbose_name="Группа",
                              on_delete=models.CASCADE,
                              null=True,
                              blank=True)

    category_income = models.ForeignKey(CategoryIncome,
                                        verbose_name="Категория прихода",
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True)

    category_outcome = models.ForeignKey(CategoryOutcome,
                                         verbose_name="Категория расхода",
                                         on_delete=models.CASCADE,
                                         null=True,
                                         blank=True)

    cashless = models.BooleanField("Безнал", default=False)

    comment = models.TextField("Комментарий", null=True, blank=True)

    def __str__(self):
        return f"{self.hotel}"

    class Meta:
        verbose_name = "Касса"
