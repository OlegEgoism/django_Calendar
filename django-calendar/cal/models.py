from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Event(models.Model):
    """Календарь"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    start_time = models.DateTimeField(verbose_name='Время начала')
    end_time = models.DateTimeField(verbose_name='Время окончания')
    user = models.ForeignKey('User', verbose_name='ФИО', related_name='user_event', on_delete=models.CASCADE,
                             blank=True, null=True)

    class Meta:
        verbose_name = 'Календарь'
        verbose_name_plural = 'Календарь'
        ordering = 'start_time',

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.start_time.__format__("%H:%M")} - {self.user}</a>'  # <hr>'

    def clean(self):
        """Проверка даты"""
        if self.end_time <= self.start_time:
            raise ValidationError('Дата окончания должна быть позже даты начала.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class User(models.Model):
    """Пользователь"""
    name = models.CharField(verbose_name='ФИО', max_length=200)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
        ordering = 'name',

    def __str__(self):
        return self.name

    def count_user_event(self):
        return self.user_event.count()

    count_user_event.short_description = 'Всего мероприятий'
