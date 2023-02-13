from django.shortcuts import render, redirect
from django.views import View

from crm.forms import BookingGroupForm
from crm.models import Group


class IndexView(View):

    def get(self, request):
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
            group = form.save()
            return redirect('group', pk=group.pk)
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


class GroupsView(View):
    @staticmethod
    def get(request):
        groups = Group.objects.all()
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
