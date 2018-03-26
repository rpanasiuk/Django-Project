from django.shortcuts import render
from django.http import Http404

from .models import ProductType

def bootstrap(request):
	try:
		instance = ProductType.objects.all()[0].product_class.all()
	except ProductType.DoesNotExist:
		raise Http404

	if instance:
		context = {'footwear': instance}
	else:
		context = {'footwear': 'There is no shoes.'}
	print(context)
	return render(request, 'bootstrap/bootstrap_example.html', context)
