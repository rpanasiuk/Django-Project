from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView
from django.db.models import Q

from .models import ProductType, Product

class ProductTypeNavListView(ListView):
	model = ProductType
	template_name = 'base.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProductTypeNavListView, self).get_context_data(*args, **kwargs)
		male_obj = ProductType.objects.get(name='Footwear', sex='Male')
		context['male_categories'] = male_obj.category.all()
		female_obj = ProductType.objects.get(name='Footwear', sex='Female')
		context['female_categories'] = female_obj.category.all()

		return context

class ProductSearchListView(ListView):
	model = Product
	template_name = 'products/search.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProductSearchListView, self).get_context_data(*args, **kwargs)
		qs = self.request.GET.get('q', None)
		print(qs)
		prod = Product.objects.search(qs)
		if qs:
			context['products_all'] = prod

		return context