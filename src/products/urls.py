from django.contrib import admin
from django.urls import path

from .views import ProductSearchListView, ProductDetailView

app_name = 'products'

urlpatterns = [
	path('search/', ProductSearchListView.as_view(), name='search_list'),
	path('<slug>/', ProductDetailView.as_view(), name='detail'),
]