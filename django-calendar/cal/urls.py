
from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path('info/', views.info, name='info'),
    # path('allres/', views.allres, name='allres'),
    # path("delete/<int:id>", delete, name='delete'),


    path('index/', views.index, name='index'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<int:id>/', views.event, name='event_edit'),
    path('event/delete/<int:pk>/', views.EventMemberDeleteView.as_view(), name="event_delete"),

    # path('event/delete/<int:id>/', views.delete, name='event_delete'),



	# path('event/edit/(?P<event_id>\d+)/', views.event, name='event_edit'),
    # path('event/delete/(?P<event_id>\d+)/', views.delete, name='delete'),

    # path("event/delete/<int:id>", delete, name='delete'),
]
