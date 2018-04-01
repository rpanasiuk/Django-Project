from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.db.models import Q

from .models import ProductType, Product, Category


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
		slug = self.kwargs.get('slug')
		obj = Product.objects.get_product_by_id(slug)
		if obj:
			return obj
		else:
			raise Http404

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		prod = self.get_object()
		context['object'] = prod

		return context

class ProductListView(ListView):
	model = Product
	template_name = 'products/product-list.html'

	def get_queryset(self, *args, **kwargs):
		product_class = self.kwargs.get('prod_class', None)
		sex = self.kwargs.get('sex', None)
		print(self.kwargs)
		if sex and product_class:
			queryset = Product.objects.filter(
				Q(product_class__name__iexact=product_class) &
				Q(product_class__sex__iexact=sex)
			)
		if not sex and product_class:
			queryset = Product.objects.filter(
				Q(product_class__name__iexact=product_class)
			)
		elif sex and not product_class:
			queryset = Product.objects.filter(
				Q(product_class__sex__iexact=sex)
			)
		else:
			queryset = super(ProductListView, self).get_queryset(*args, **kwargs)

		return queryset

	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		qs = self.get_queryset()
		cat = self.kwargs.get('category')
		if cat:
			cat = Category.objects.get(name=cat)
			qs = qs.filter(category=cat)
		context['products'] = qs

		return context