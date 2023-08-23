from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/new/', views.event, name='event_new'),
    path('event/edit/<int:id>/', views.event, name='event_edit'),
    path('event/delete/<int:pk>/', views.EventMemberDeleteView.as_view(), name="event_delete"),
    path('list_user/', views.list_user, name='list_user'),
    path('add_user/', views.add_user, name='add_user'),
    path('user_detail/<int:user_id>/', views.user_detail, name='user_detail'),
]
