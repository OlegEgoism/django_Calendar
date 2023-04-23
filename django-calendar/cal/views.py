from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import DeleteView
from django.utils.safestring import mark_safe
import locale
import calendar
from .models import *
from .utils import Calendar
from .forms import EventForm, CrForm

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')  # Установите локаль на русский язык


def index(request):
    return HttpResponse('hello')


def info(request):
    return HttpResponse('Для редактирования')


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        return context


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, id=None):
    # instance = Event()
    # event_del = Event.objects.get(id=id)


    if id:
        instance = get_object_or_404(Event, id=id)

    else:
        instance = Event()
        # event_del = Event.objects.get(id=id)
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))

    context = {
        'form': form,
        'event_del': instance,
    }
    return render(request, 'cal/event.html', context=context)


class EventMemberDeleteView(DeleteView):
    model = Event
    template_name = "cal/event_delete.html"
    success_url = reverse_lazy("cal:calendar")


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     event_del = Event.objects.get(id=id)
    #     context['calendar'] = mark_safe(event_del)


# def delete(request, id):
#     try:
#         event_del = Event.objects.get(id=id)
#         event_del.delete()
#         # return render(request, 'cal/event_delete.html', {'event_del': event_del})
#         return HttpResponseRedirect(reverse('cal:calendar'))
#     except Event.DoesNotExist:
#         return HttpResponseNotFound("<h2>НЕТ ЗАПИСИ!!!</h2>")


# <a class="btn btn-info right" href="{% url 'cal:event_delete' %}">Удaлить</a>


# # удаление данных иэ БД
# def delete(request, id):
#     person = Event.objects.get(id=id)
#     person.delete()
#     return render(request, 'cal/event.html', {'person': person})
#     # try:
#     #     person = Event.objects.get(id=id)
#     #     person.delete()
#     #     return HttpResponseRedirect(reverse('cal:calendar'))
#     #     return HttpResponseRedirect("/")
#     # except Event.DoesNotExist:
#     #     return render(request, 'cal/event.html')
#
#
# def info(request):
#     info = Event.objects.all()
#     form = CrForm(request.POST or None)  # , instance=instance)
#     if request.POST and form.is_valid():
#         form.save()
#         return HttpResponseRedirect(reverse('cal:info'))
#     contesxt = {
#         'info': info,
#         'form': form,
#     }
#     return render(request, 'cal/info.html', contesxt)
#
#
# def allres(request):
#     info = Event.objects.all()
#     contesxt = {
#         'info': info,
#         # 'form': form,
#     }
#     return render(request, 'cal/allres.html', contesxt)
