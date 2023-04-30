from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Employee, Position, Room, Hotel, Groceries, Household, InventoryControl, Group, Booking, Guest, \
    CategoryIncome, CategoryOutcome
from django.contrib.auth.admin import UserAdmin


class EmployeesAdmin(UserAdmin):
    model = Employee
    list_display = ("username", "first_name", "last_name", "position",)
    fieldsets = (
        (None, {"fields": ("username", "password", "email")}),
        (None, {"fields": ("first_name", "last_name", "position", "hotel")},),
        (None, {"fields": ("is_superuser", "is_staff", "is_active", "groups")}))


class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


class RoomAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "hotel", "capacity", "over_booking", "price", "fullness", "grouped_hotel")
    list_filter = ("hotel",)
    search_fields = ("number", "name", "hotel__name")

    def grouped_hotel(self, obj):
        return obj.hotel.name

    grouped_hotel.short_description = "Отель"


class HotelAdmin(admin.ModelAdmin):
    list_display = ("name", "display_rooms")

    def display_rooms(self, obj):
        rooms = Room.objects.filter(hotel=obj)
        room_links = [f'<a href="{reverse("admin:crm_room_change", args=[room.id])}">{room.number}</a>' for room in
                      rooms]
        return format_html(", ".join(room_links))

    display_rooms.short_description = 'Номера'


class GroceriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'price', 'unit')
    list_filter = ('unit',)
    search_fields = ('name', 'count', 'price')


class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('name', 'count', 'price', 'unit')
    list_filter = ('unit',)
    search_fields = ('name', 'count', 'price')


class InventoryControlAdmin(admin.ModelAdmin):
    list_display = ('goods', 'date_update', 'user', 'count')
    list_filter = ('user', 'date_update')
    search_fields = ('goods', 'count', 'user')


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'count_guests', 'tag', 'group_organizer', 'date_checkin', 'date_checkout', 'hotel')


class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest', 'room', 'date_checkin', 'date_checkout')


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'telephone', 'group', 'room')


class CategoryIncomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class CategoryOutcomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(CategoryIncome, CategoryIncomeAdmin)
admin.site.register(CategoryOutcome, CategoryOutcomeAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(InventoryControl, InventoryControlAdmin)
admin.site.register(Household, HouseholdAdmin)
admin.site.register(Groceries, GroceriesAdmin)
admin.site.register(Employee, EmployeesAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Hotel, HotelAdmin)
