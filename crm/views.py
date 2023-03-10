from django.shortcuts import render, redirect
from django.views import View

from crm.forms import BookingGroupForm, KitchenForm, KitchenUpdateForm, HouseholdForm, HouseholdUpdateForm
from crm.helpers import change_fullness, get_title_object_info, get_equivalent_products, get_products
from crm.models import Group, Hotel, Room, Goods, Groceries, Household


class IndexView(View):

    @staticmethod
    def get(request):
        objects = Hotel.objects.all()
        for obj in objects:
            get_title_object_info(obj)
        context = {
            "objects": objects,
        }
        return render(request, "crm/objects.html", context)


class ObjectView(View):
    @staticmethod
    def get(request, pk):
        # todo get data for page with object
        hotel = Hotel.objects.get(pk=pk)
        rooms = Room.objects.filter(hotel=hotel)

        context = {
            "hotel": hotel,
            "rooms": rooms,
        }
        return render(request, "crm/object.html", context)


class ReportPeriodView(View):
    def get(self, request):
        return render(request, "crm/report_period.html")


class ReportGroupView(View):
    def get(self, request):
        return render(request, "crm/report_group.html")


class ReportInlineView(View):
    def get(self, request):
        return render(request, "crm/report_inline.html")


class EarlyBookingGroupView(View):
    @staticmethod
    def get(request):
        form = BookingGroupForm()
        context = {
            "form": form,
        }
        return render(request, "crm/early_booking.html", context)

    @staticmethod
    def post(request):
        form = BookingGroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("groups")
        else:
            context = {
                "form": form,
            }
            return render(request, "crm/early_booking.html", context)


class BookingGroupView(View):
    @staticmethod
    def get(request):
        return render(request, "crm/booking_group.html")


class BookingGuestView(View):
    def get(self, request):
        return render(request, "crm/booking_guest.html")


class WarehouseAccountingView(View):
    @staticmethod
    def get(request):
        form = HouseholdForm()
        products = get_products(Household)
        form_update = HouseholdUpdateForm()
        context = {
            "form": form,
            "products": products,
            "form_update": form_update,
        }
        return render(request, "crm/warehouse_accounting.html", context)

    @staticmethod
    def post(request):
        form = HouseholdForm(request.POST)
        form_update = HouseholdUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("warehouse-accounting")

        else:
            products = get_products(Household)
            context = {
                "form": form,
                "products": products,
                "form_update": form_update,
            }
            return render(request, "crm/warehouse_accounting.html", context)


class WarehouseUpdateView(View):
    @staticmethod
    def post(request):
        form = HouseholdUpdateForm(request.POST)
        if form.is_valid():
            product = Goods.objects.get(pk=request.POST.get("id"))
            product.how_many_unit = form.cleaned_data.get("how_many_unit")
            product.price = form.cleaned_data.get("price")
            product.save()
            return redirect("warehouse-accounting")
        else:
            context = {
                "form": form,
            }
            return render(request, "crm/kitchen_accounting.html", context)


class KitchenAccountingView(View):
    @staticmethod
    def get(request):
        form = KitchenForm()
        products = get_products(Groceries)
        form_update = KitchenUpdateForm()
        context = {
            "form": form,
            "products": products,
            "form_update": form_update,
        }
        return render(request, "crm/kitchen_accounting.html", context)

    @staticmethod
    def post(request):
        form = KitchenForm(request.POST)
        form_update = KitchenUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("kitchen-accounting")

        else:
            products = get_products(Groceries)
            context = {
                "form": form,
                "products": products,
                "form_update": form_update,
            }
            return render(request, "crm/kitchen_accounting.html", context)


class KitchenUpdateView(View):
    @staticmethod
    def post(request):
        form = KitchenUpdateForm(request.POST)
        if form.is_valid():
            product = Goods.objects.get(pk=request.POST.get("id"))
            product.how_many_unit = form.cleaned_data.get("how_many_unit")
            product.price = form.cleaned_data.get("price")
            product.save()
            return redirect("kitchen-accounting")
        else:
            context = {
                "form": form,
            }
            return render(request, "crm/kitchen_accounting.html", context)


class CalendarHallView(View):
    def get(self, request):
        return render(request, "crm/calendar_hall.html")


class CalendarSaunaView(View):
    def get(self, request):
        return render(request, "crm/calendar_sauna.html")


class CashierIncomeView(View):
    def get(self, request):
        return render(request, "crm/cashier_income.html")


class CashierOutcomeView(View):
    def get(self, request):
        return render(request, "crm/cashier_outcome.html")


class GuestsView(View):
    def get(self, request):
        return render(request, "crm/guests.html")


class GuestView(View):
    def get(self, request, pk):
        guest = Hotel.objects.get(pk=pk)
        context = {
            "guest": guest,
        }
        return render(request, "crm/guest.html", context)


class GroupsView(View):
    @staticmethod
    def get(request):
        groups = Group.objects.all().order_by("date_checkin")
        context = {
            "groups": groups,
        }
        return render(request, "crm/groups.html", context)


class GroupView(View):
    def get(self, request, pk):
        group = Group.objects.get(pk=pk)
        context = {
            "group": group,
        }
        return render(request, "crm/group.html", context)
