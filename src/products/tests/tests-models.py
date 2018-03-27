from django.test import TestCase

from products.models import Category, Product, ProductType

class CategoryModelTest(TestCase):

	@classmethod
	def setUpTestData(cls):
		Category.objects.create(name='Air Max')
		Category.objects.create(name='Jordan')

	def test_name_getting(self):
		category = Category.objects.first().name
		self.assertEquals(category, 'Air Max')

class ProductTypeModelTest(TestCase):

	def setUp(self):
		prod_type_female = ProductType.objects.create(name='Footwear', sex='Female')
		prod_type_male = ProductType.objects.create(name='Footwear', sex='Male')
		for cat in ['Air Max', 'Jordan', 'Runners']:
			Category.objects.create(name=cat)
		obj1 = Category.objects.all()[:2]
		obj2 = Category.objects.all()[2]

		prod_type_female.category.set(obj1)
		prod_type_male.category.add(obj2)

	def test_get_all_female_categories(self):
		gender = ProductType.objects.get(name='Footwear', sex='Female')
		categories = gender.category.all()
		self.assertQuerysetEqual(categories, 
			['<Category: Air Max>', '<Category: Jordan>'], ordered=False)