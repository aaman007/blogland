from django.urls import path

from core.api.views import PingAPI, BlogListAPIView, TestAPI

app_name = 'core'

urlpatterns = [
    path('ping/', PingAPI.as_view(), name='ping'),
    path('posts/', BlogListAPIView.as_view(), name='posts'),
    path('test/', TestAPI.as_view(), name='test')
]
