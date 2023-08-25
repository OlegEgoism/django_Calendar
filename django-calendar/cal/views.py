from datetime import datetime, timedelta, date
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
import locale
import calendar
from .models import *
from .utils import Calendar
from .forms import EventForm, UserForm

locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')  # Установите локаль на русский язык
calendar.month_name = ['',
                       'ЯНВАРЬ', 'ФЕВРАЛЬ', 'МАРТ',
                       'АПРЕЛЬ', 'МАЙ', 'ИЮНЬ',
                       'ИЮЛЬ', 'АВГУСТ', 'СЕНТЯБРЬ',
                       'ОКТЯБРЬ', 'НОЯБРЬ', 'ДЕКАБРЬ'
                       ]


class CalendarView(generic.ListView):
    """Календарь"""
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
        users_with_colors = User.objects.all().values('id', 'color')
        context['users_with_colors'] = {user['id']: user['color'] for user in users_with_colors}
        return context


def get_date(req_month):
    """Обработка даты"""
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    """Предыдущий месяц"""
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    """Следующий месяц"""
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event(request, id=None):
    """Просмотр и редактирование мероприятия"""
    instance = get_object_or_404(Event, id=id) if id else Event()
    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))

    context = {
        'form': form,
        'event_del': instance,
    }
    return render(request, 'cal/event.html', context=context)


def event_delete(request, event_id):
    """Удаление мероприятия"""
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect(reverse('cal:calendar'))

    context = {
        'event': event,
    }
    return render(request, 'cal/event_delete.html', context)


def user_list(request):
    """Список пользователей"""
    users_with_event_count = User.objects.annotate(event_count=Count('user_event'))
    total_event_count = Event.objects.count()
    context = {
        'users_with_event_count': users_with_event_count,
        'total_event_count': total_event_count
    }
    return render(request, 'cal/user_list.html', context)


def add_user(request):
    """Добовляение пользователя"""
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('cal:calendar'))
    else:
        user_form = UserForm()
    context = {
        'user_form': user_form,
    }
    return render(request, 'cal/add_user.html', context=context)


def user_detail(request, user_id):
    """Информмация о пользователе"""
    user = User.objects.get(pk=user_id)
    all_event = user.user_event.all()
    if request.method == 'POST':
        user.delete()
        return redirect('cal:user_list')
    context = {
        'user': user,
        'all_event': all_event
    }
    return render(request, 'cal/user_detail.html', context)


def user_delete(request, user_id):
    """Удаляем выброного пользователя"""
    user = get_object_or_404(User, pk=user_id)
    context = {
        'user': user,
    }
    return render(request, 'cal/user_delete.html', context)
