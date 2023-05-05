from datetime import timedelta, datetime
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from crm.forms import BookingGroupForm, KitchenForm, KitchenUpdateForm, HouseholdForm, HouseholdUpdateForm, \
    IncomeForm, OutcomeForm
from crm.helpers import get_products, validate_date, get_booking, get_date_for_report
from crm.models import Group, Hotel, Room, Goods, Groceries, Household, InventoryControl, Employee, Guest, Cashier


class IndexView(View):

    @staticmethod
    def get(request):
        hotels = Hotel.objects.all()
        rooms = Room.objects.all()
        start_date, end_date = validate_date(request)
        objects = []
        for hotel in hotels:
            objects.append(get_booking(hotel, start_date, end_date, rooms))

        context = {
            "objects": objects,
        }
        return render(request, "crm/objects.html", context)


class ObjectView(View):
    @staticmethod
    def get(request, pk):
        hotel = Hotel.objects.get(pk=pk)
        rooms = Room.objects.filter(hotel=hotel)
        start_date, end_date = validate_date(request)
        title_object_info = get_booking(hotel, start_date, end_date, rooms)

        # получаем информацию о загружености отеля
        full = title_object_info.fullness_hotel
        number_guest_in_hotel = title_object_info.number_guest_in_hotel

        # получаем информацию о загружености отеля по датам
        delta = timedelta(days=1)

        object_info_by_date = []
        while start_date <= end_date:
            object_info_by_date.append([start_date, get_booking(hotel, start_date, end_date, rooms), end_date])
            start_date += delta

        groups = title_object_info.group_set.all()
        employees = title_object_info.employee_set.all()

        context = {
            "title_object_info": title_object_info,
            "rooms": rooms,
            "groups": groups,
            "employees": employees,
            "full": full,
            "number_guest_in_hotel": number_guest_in_hotel,
            "object_info_by_date": object_info_by_date,
        }
        return render(request, "crm/object.html", context)


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

    def post(self, request):
        form = HouseholdUpdateForm(request.POST)
        if form.is_valid():
            self._update_product(request, form)
            return redirect("warehouse-accounting")
        else:
            context = {
                "form": form,
            }
            return render(request, "crm/kitchen_accounting.html", context)

    @staticmethod
    def _update_product(request, form):
        inventory_control = InventoryControl()
        goods = Goods.objects.get(pk=request.POST.get("id"))
        goods.how_many_unit = form.cleaned_data.get("how_many_unit")
        goods.price = form.cleaned_data.get("price")
        inventory_control.goods = goods
        inventory_control.user = request.user
        inventory_control.count = form.cleaned_data.get("how_many_unit")
        goods.save()
        inventory_control.save()


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


class ReportView(View):
    @staticmethod
    def get(request):
        start_date, finish_date = get_date_for_report(request)

        balances = (
            Cashier.objects.filter(date_service__lte=start_date, date_service__gte=finish_date)
            .values("date_service")
            .annotate(
                total_incomes=Coalesce(Sum("incomes"), 0),
                total_outcomes=Coalesce(Sum("outcomes"), 0),
                balance=Coalesce(Sum("incomes"), 0) - Coalesce(Sum("outcomes"), 0),
            )
            .order_by("date_service")
        )

        context = {
            "balances": balances,
            "start_date": start_date,
            "finish_date": finish_date,
        }
        print(start_date, finish_date)
        return render(request, "crm/report.html", context)


class ReportDetail(View):
    @staticmethod
    def get(request, date):
        date = datetime.strptime(date, "%Y-%m-%d")
        cashier_categories = Cashier.objects.filter(date_service=date).order_by("category_outcome", "category_income")

        incomes = (
            Cashier.objects
            .all()
            .filter(date_service=date)
            .exclude(incomes=0)
            .values("incomes", "category_income__name", "guest__first_name", "guest__last_name", "employee__first_name",
                    "employee__last_name")
            .order_by("category_income"))

        outcomes = (
            Cashier.objects
            .all()
            .filter(date_service=date)
            .exclude(outcomes=0)
            .values("outcomes", "category_outcome__name", "guest__first_name", "guest__last_name",
                    "employee__first_name", "employee__last_name")
            .order_by("category_outcome"))

        total_incomes = Cashier.objects.filter(date_service=date).aggregate(Sum('incomes'))
        total_outcomes = Cashier.objects.filter(date_service=date).aggregate(Sum('outcomes'))

        sum_incomes = total_incomes['incomes__sum'] or 0
        sum_outcomes = total_outcomes['outcomes__sum'] or 0

        context = {
            "date_report": date,
            "cashier_categories": cashier_categories,
            "incomes": incomes,
            "outcomes": outcomes,
            "sum_incomes": sum_incomes,
            "sum_outcomes": sum_outcomes,
        }
        return render(request, "crm/report-detail.html", context)


class BookingGroupView(View):
    @staticmethod
    def get(request):
        return render(request, "crm/booking_group.html")


class BookingGuestView(View):
    @staticmethod
    def get(request):
        return render(request, "crm/booking_guest.html")


class CalendarHallView(View):
    @staticmethod
    def get(request):
        return render(request, "crm/calendar_hall.html")


class CalendarSaunaView(View):
    @staticmethod
    def get(request):
        return render(request, "crm/calendar_sauna.html")


class CashierIncomeView(View):
    @staticmethod
    def get(request):
        form = IncomeForm()

        context = {
            "form": form,
        }
        return render(request, "crm/cashier_income.html", context)

    @staticmethod
    def post(request):
        form = IncomeForm(request.POST)

        if form.is_valid():

            form.save()
            return redirect("report")
        else:
            form = IncomeForm()

            print(form.errors)

            return render(request, "crm/cashier_income.html", {"form": form})


class CashierOutcomeView(View):
    @staticmethod
    def get(request):
        form = OutcomeForm()
        context = {
            "form": form,
        }
        return render(request, "crm/cashier_outcome.html", context)

    @staticmethod
    def post(request):
        form = OutcomeForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect("report")
        else:
            form = OutcomeForm()
            print(form.errors)

            return render(request, "crm/cashier_outcome.html", {"form": form})


class GuestsView(View):
    @staticmethod
    def get(request):
        return render(request, "crm/guests.html")


class GuestView(View):
    @staticmethod
    def get(request, pk):
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
    @staticmethod
    def get(request, pk):
        group = Group.objects.get(pk=pk)
        context = {
            "group": group,
        }
        return render(request, "crm/group.html", context)


class HotelView(View):
    @staticmethod
    def post(request, pk):
        context = {}
        employees = Employee.objects.filter(hotel__id=pk)
        customers = Guest.objects.filter(booking__room__hotel=pk, in_hotel=True)

        staff = {}
        guests = {}

        for employee in employees:
            staff[employee.id] = f"{employee.first_name} {employee.last_name}"
        for customer in customers:
            guests[customer.id] = f"{customer.first_name} {customer.first_name}"
        context["employees"] = staff
        context["customers"] = guests
        return JsonResponse(context, json_dumps_params={"ensure_ascii": False})
