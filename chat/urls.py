from django.urls import path
from . import views


urlpatterns = [
    path('messages/<int:sender>/<int:receiver>/<int:new>', views.MessageView.as_view(), name='messages-new'),
    path('messages/<int:sender>/<int:receiver>', views.MessageView.as_view(), name='messages-read'),
    path('messages', views.MessageView.as_view(), name='messages-post')
]
