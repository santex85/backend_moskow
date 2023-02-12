from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('booking-groups/', views.BookingGroups.as_view(), name='booking_groups'),
]
