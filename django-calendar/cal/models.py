from django.db import models
from django.urls import reverse


class Event(models.Model):
    """Календарь учителя"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    start_time = models.DateTimeField(verbose_name='Время начала', blank=True, null=True)
    end_time = models.DateTimeField(verbose_name='Время окончания', blank=True, null=True)
    user = models.ForeignKey('User', verbose_name='ФИО', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Календарь учителя'
        verbose_name_plural = 'Календарь учителя'
        ordering = 'start_time',

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.start_time.__format__("%H:%M")} - {self.user}</a>'  # <hr>'


class User(models.Model):
    name = models.CharField(verbose_name='ФИО', max_length=200)

    def __str__(self):
        return self.name
