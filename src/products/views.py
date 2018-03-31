from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404

from .models import ProductType, Product


class ProductSearchListView(ListView):
	model = Product
	template_name = 'products/search.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProductSearchListView, self).get_context_data(*args, **kwargs)
		qs = self.request.GET.get('q', None)
		prod = Product.objects.search(qs)
		if qs:
			context['products_all'] = prod

		return context

class ProductDetailView(DetailView):
	model = Product
	template_name = 'products/detail.html'

	def get_object(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		obj = Product.objects.get_product_by_id(pk)
		if obj:
			return obj
		else:
			raise Http404