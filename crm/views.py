from django.shortcuts import render
from django.views import View

from crm.forms import BookingGroupForm


class BookingGroups(View):
    @staticmethod
    def get(request):
        form = BookingGroupForm()
        context = {
            'form': form,
        }
        return render(request, 'crm/booking.html', context)

    @staticmethod
    def post(request):
        form = BookingGroupForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            form = BookingGroupForm()
        context = {
            "form": form,
        }
        return render(request, 'crm/booking.html', context)
