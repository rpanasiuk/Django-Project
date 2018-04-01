from django.contrib import admin
from django.urls import path, include

from .views import ProductSearchListView, ProductDetailView, ProductListView

app_name = 'products'

prod_class_patterns = ([
	path('', ProductListView.as_view(), name='all'),
	path('<sex>/', ProductListView.as_view(), name='sex'),
	path('<sex>/<category>', ProductListView.as_view(), name='category'),
], 'p_class')

urlpatterns = [
	path('search/', ProductSearchListView.as_view(), name='search_list'),
	path('<prod_class>/', include(prod_class_patterns)),
]

