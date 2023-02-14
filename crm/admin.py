from django.contrib import admin
from .models import Employee, Position, Room, Hotel
from django.contrib.auth.admin import UserAdmin


class EmployeesAdmin(UserAdmin):
    model = Employee
    list_display = ('username', 'first_name', 'last_name', 'position',)
    fieldsets = (
        (None, {"fields": ('username', 'password', 'email')}),
        (None, {"fields": ('first_name', 'last_name', 'position')},),
        (None, {"fields": ('is_superuser', 'is_staff', 'is_active', 'groups')}))


admin.site.register(Employee, EmployeesAdmin)


class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Position, PositionAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'hotel', 'capacity', 'over_booking', 'price', 'fullness')


class HotelAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Room, RoomAdmin)
admin.site.register(Hotel, HotelAdmin)
