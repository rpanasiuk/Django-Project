from django.shortcuts import render
from django.http import Http404
from django.views.generic import ListView
from django.db.models import Q

from .models import ProductType, Product

# def bootstrap(request):
# 	try:
# 		instance = ProductType.objects.all()[0].product_class.all()
# 	except ProductType.DoesNotExist:
# 		raise Http404

# 	if instance:
# 		context = {'footwear': instance}
# 	else:
# 		context = {}
# 	print(context)
# 	return render(request, 'bootstrap/bootstrap_example.html', context)

class ProductTypeNavListView(ListView):
	model = ProductType
	template_name = 'bootstrap/bootstrap_example.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProductTypeNavListView, self).get_context_data(*args, **kwargs)
		male_obj = ProductType.objects.get(name='Footwear', sex='Male')
		context['male_categories'] = male_obj.category.all()
		female_obj = ProductType.objects.get(name='Footwear', sex='Female')
		context['female_categories'] = female_obj.category.all()
		print('123')

		return context

class ProductSearchListView(ListView):
	model = Product
	template_name = 'products/producttype_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(ProductSearchListView, self).get_context_data(*args, **kwargs)
		print('context: ', context)
		query = self.request.GET.get('q')
		print('query: ', query)
		context['query'] = query

		return context

	def get_queryset(self, *args, **kwargs):
		queryset = super(ProductSearchListView, self).get_queryset(*args, **kwargs)
		qs = self.request.GET.get('q', None)
		if qs:
			queryset = self.objects.filter(
				Q(title__icontains=qs) |
				Q(price__icontains=qs) |
				Q(description__icontains=qs) |
				Q(category__name__icontains=qs) |
				Q(product_class__icontains=qs)
				).discinct()
			print(queryset)
		return qs


