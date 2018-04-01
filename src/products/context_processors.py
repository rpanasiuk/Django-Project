from .models import ProductType

def get_all_categories(request):
	try:
		male_obj = ProductType.objects.get(name='Footwear', sex='Male')
		female_obj = ProductType.objects.get(name='Footwear', sex='Female')
	except ProductType.DoesNotExist:
		pass

	dict_ = {
		'product_class': male_obj.name,
		'male': male_obj.sex,
		'female': female_obj.sex,
		'male_categories': male_obj.category.all(),		
		'female_categories': female_obj.category.all(),		
	}

	return dict_