from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notifications-list'),
    path('<int:pk>/mark-read/', views.mark_notification_read, name='notification-mark-read'),
]
