from django.contrib import admin
from django.urls import path, include

from django.views.generic import TemplateView

from products.views import (
    ProductDetailView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html')),
    path('p/', include("products.urls", namespace='products')),
    path('account/', include('registration.backends.simple.urls')),
    path('<slug>/', ProductDetailView.as_view(), name='detail'),
]
