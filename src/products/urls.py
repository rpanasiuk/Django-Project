from django.contrib import admin
from django.urls import path

from .views import ProductSearchListView

app_name = 'products'

urlpatterns = [
	path('', ProductSearchListView.as_view(), name='search_list'),
]