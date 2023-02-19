from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('report-period/', views.ReportPeriodView.as_view(), name="report-period"),
    path('report-group/', views.ReportGroupView.as_view(), name="report-group"),
    path('report-inline/', views.ReportInlineView.as_view(), name="report-inline"),
    path('early-booking-group/', views.EarlyBookingGroupView.as_view(), name="early-booking-group"),
    path('booking-group/', views.BookingGroupView.as_view(), name="booking-group"),
    path('booking-guest/', views.BookingGuestView.as_view(), name="booking-guest"),
    path('warehouse-accounting/', views.WarehouseAccountingView.as_view(), name="warehouse-accounting"),
    path('warehouse-update/', views.WarehouseUpdateView.as_view(), name="warehouse-update"),
    path('kitchen-accounting/', views.KitchenAccountingView.as_view(), name="kitchen-accounting"),
    path('kitchen-update/', views.KitchenUpdateView.as_view(), name="kitchen-update"),
    path('calendar-hall/', views.CalendarHallView.as_view(), name="calendar-hall"),
    path('calendar-sauna/', views.CalendarSaunaView.as_view(), name="calendar-sauna"),
    path('cashier-income/', views.CashierIncomeView.as_view(), name="cashier-income"),
    path('cashier-outcome/', views.CashierOutcomeView.as_view(), name="cashier-outcome"),
    path('guests/', views.GuestsView.as_view(), name="guests"),
    path('groups/', views.GroupsView.as_view(), name="groups"),
    path('group/<pk>', views.GroupView.as_view(), name="group"),
    path('object/<pk>', views.ObjectView.as_view(), name="object"),
]
