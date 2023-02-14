from django.contrib import admin
from .models import Employee, Position
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
