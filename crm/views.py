import random

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import View
from faker import Faker

from crm.forms import BookingGroupForm
from crm.helpers import change_fullness, get_title_object_info
from crm.models import Group, Hotel, Room


class IndexView(View):

    def get(self, request):
        # todo create main page q: what is the main page?
        # fake = Faker()
        #
        # # Создаем 5 отелей
        # hotels = [Hotel.objects.create(name=fake.company()) for _ in
        #           range(5)]
        #
        # # Создаем 50 номеров (10 номеров на каждый отель)
        # for hotel in hotels:
        #     for i in range(10):
        #         name = fake.word() + " Room"
        #         capacity = random.choice([2, 3, 4])
        #         price = random.randint(50, 200)
        #         fullness = random.choice(["full", "partially", "empty"])
        #         number_guests = random.randint(0, capacity)
        #         over_booking = random.randint(0, 2)
        #         Room.objects.create(name=name, hotel=hotel, capacity=capacity, price=price, fullness=fullness,
        #                             number_guests=number_guests, over_booking=over_booking)
        return render(request, 'crm/index.html')


class ReportPeriodView(View):
    def get(self, request):
        return render(request, 'crm/report_period.html')


class ReportGroupView(View):
    def get(self, request):
        return render(request, 'crm/report_group.html')


class ReportInlineView(View):
    def get(self, request):
        return render(request, 'crm/report_inline.html')


class EarlyBookingGroupView(View):
    @staticmethod
    def get(request):
        form = BookingGroupForm()
        context = {
            'form': form,
        }
        return render(request, 'crm/early_booking.html', context)

    @staticmethod
    def post(request):
        form = BookingGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('groups')
        else:
            context = {
                "form": form,
            }
            return render(request, 'crm/early_booking.html', context)


class BookingGroupView(View):
    @staticmethod
    def get(request):
        return render(request, 'crm/booking_group.html')


class BookingGuestView(View):
    def get(self, request):
        return render(request, 'crm/booking_guest.html')


class WarehouseAccountingView(View):
    def get(self, request):
        return render(request, 'crm/warehouse_accounting.html')


class KitchenAccountingView(View):
    def get(self, request):
        return render(request, 'crm/kitchen_accounting.html')


class CalendarHallView(View):
    def get(self, request):
        return render(request, 'crm/calendar_hall.html')


class CalendarSaunaView(View):
    def get(self, request):
        return render(request, 'crm/calendar_sauna.html')


class CashierIncomeView(View):
    def get(self, request):
        return render(request, 'crm/cashier_income.html')


class CashierOutcomeView(View):
    def get(self, request):
        return render(request, 'crm/cashier_outcome.html')


class GuestsView(View):
    def get(self, request):
        return render(request, 'crm/guests.html')


class GuestView(View):
    def get(self, request, pk):
        guest = Hotel.objects.get(pk=pk)
        context = {
            'guest': guest,
        }
        return render(request, 'crm/guest.html', context)


class GroupsView(View):
    @staticmethod
    def get(request):
        groups = Group.objects.all().order_by('date_checkin')
        context = {
            'groups': groups,
        }
        return render(request, 'crm/groups.html', context)


class GroupView(View):
    def get(self, request, pk):
        group = Group.objects.get(pk=pk)
        context = {
            'group': group,
        }
        return render(request, 'crm/group.html', context)


class ObjectsView(View):
    @staticmethod
    def get(request):
        objects = Hotel.objects.all()
        # todo
        for obj in objects:
            get_title_object_info(obj)
        context = {
            'objects': objects,
        }
        print(context)
        return render(request, 'crm/objects.html', context)


class ObjectView(View):
    @staticmethod
    def get(request, pk):
        # todo get data for page with object
        hotel = Hotel.objects.get(pk=pk)
        context = {
            'hotel': hotel,
        }
        return render(request, 'crm/object.html', context)
