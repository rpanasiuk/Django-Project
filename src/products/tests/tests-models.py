from django.test import TestCase
from django.db.utils import IntegrityError

from products.models import Category, Product, ProductType

def model_setup():
		prod_type_female = ProductType.objects.create(name='Footwear', sex='Female')
		prod_type_male = ProductType.objects.create(name='Footwear', sex='Male')
		prod_type_junior = ProductType.objects.create(name='Footwear', sex='Junior')
		for cat in ['Air Max', 'Jordan', 'Runners']:
			Category.objects.create(name=cat)
		cat1 = Category.objects.all()[0]
		cat2 = Category.objects.all()[1]
		cat3 = Category.objects.all()[2]
		cat4 = Category.objects.all()[:2]
		cat5 = Category.objects.all()[1:]
		cat6 = Category.objects.all()[::2]
		cat7 = Category.objects.all()

		prod_type_female.category.set(cat4)
		prod_type_male.category.set(cat5)
		prod_type_junior.category.add(cat3)

		product_1 = Product(
			title='Air Jordan 11 Retro "Space Jam"',
			price = 2000,
			description='The Air Jordan 11 originally released in 1996\
				and is famous for its patent leather upper. The shoes were\
				designed by Tinker Hatfield and Michael Jordan himself calls\
				it his favorite Air Jordan sneaker',
			)
		product_1.save()
		prod_type_female.product_class.add(product_1)

		product_2 = Product(
			title='Nike Air Max 270',
			price = 200,
			description='Delivery takes place from 4 days after an order has been confirmed.',
			)
		product_2.save()
		prod_type_female.product_class.add(product_2)

		product_3 = Product(
			title='adidas NMD R2',
			price = 149,
			description='The adidas NMD R2 is a new low-top sneaker from adidas Originals.\
				It is the second version of the adidas NMD R1 and features a mix of Primeknit,\
				suede, and Boost cushioning. ',
			)
		product_3.save()
		prod_type_female.product_class.add(product_3)

		product_4 = Product(
			title='Reebok Classic Leather',
			price = 49.01,
			description='Delivery takes place from 4 days after an order has been confirmed.',
			)
		product_4.save()
		prod_type_male.product_class.add(product_4)

		product_5 = Product(
			title='Vans x Rains UA Old Skool Lite',
			price = 149.98,
			description='Delivery takes place from 4 days after an order has been confirmed.',
			)
		product_5.save()
		prod_type_male.product_class.add(product_5)

		product_6 = Product(
			title='Asics x asphaldgold GEL-DS Trainer OG',
			price = 309,
			description='Delivery takes place from 4 days after an order has been confirmed.',
			)
		product_6.save()
		prod_type_male.product_class.add(product_6)

		product_7 = Product(
			title='Nike Air Max 98',
			price = 200,
			description='Delivery takes place from 4 days after an order has been confirmed.',
			)
		product_7.save()
		prod_type_junior.product_class.add(product_7)

		product_8 = Product(
			title='adidas ZX750',
			price = 38,
			description='Delivery takes place from 4 days after an order has been confirmed.',
			)
		product_8.save()
		prod_type_junior.product_class.add(product_8)

		product_1.category.add(cat1)
		product_2.category.add(cat2)
		product_3.category.add(cat3)
		product_4.category.set(cat4)
		product_5.category.set(cat5)
		product_6.category.set(cat6)
		product_7.category.set(cat7)
		product_8.category.add(cat1)

class ProductModelTest(TestCase):

	def setUp(self):
		model_setup()

	def test_get_all_products_from_footwear_product_class(self):
		prod = Product.objects.filter(product_class__name='Footwear')
		self.assertQuerysetEqual(prod, 
			['<Product: Reebok Classic Leather>', 
			 '<Product: Air Jordan 11 Retro "Space Jam">',
			 '<Product: Vans x Rains UA Old Skool Lite>',
			 '<Product: Asics x asphaldgold GEL-DS Trainer OG>',
			 '<Product: Nike Air Max 270>', 
			 '<Product: adidas NMD R2>',
			 '<Product: Nike Air Max 98>',
			 '<Product: adidas ZX750>'], ordered=False
		)

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
		model_setup()
	
	def test_display_of___str___function(self):
		prod_type = ProductType.objects.filter(name='Footwear', sex='Female')
		self.assertQuerysetEqual(prod_type, 
			['<ProductType: Footwear -> Female>'], ordered=False)

	def test_unique_together_for_name_and_sex(self):
		with self.assertRaises(IntegrityError):
			ProductType.objects.create(name='Footwear', sex='Female')

	def test_get_all_female_categories(self):
		prod_type = ProductType.objects.get(name='Footwear', sex='Female')
		categories = prod_type.category.all()
		self.assertQuerysetEqual(categories, 
			['<Category: Air Max>', '<Category: Jordan>'], ordered=False)

	def test_get_all_male_products(self):
		prod_type = ProductType.objects.get(name='Footwear', sex='Male')
		products = prod_type.product_class.all()
		self.assertQuerysetEqual(products, 
			['<Product: Reebok Classic Leather>', 
			 '<Product: Vans x Rains UA Old Skool Lite>', 
			 '<Product: Asics x asphaldgold GEL-DS Trainer OG>'], ordered=False
		)		

	def test_get_all_male_products_with_respect_to_categories(self):
		prod_type = ProductType.objects.get(name='Footwear', sex='Male')
		products = prod_type.product_class.filter(category__in=prod_type.category.all())
		self.assertQuerysetEqual(products, 
			['<Product: Reebok Classic Leather>', 
			 '<Product: Vans x Rains UA Old Skool Lite>',
			 '<Product: Vans x Rains UA Old Skool Lite>',
			 '<Product: Asics x asphaldgold GEL-DS Trainer OG>'], ordered=False
		)

	def test_get_product_when_categories_do_not_match(self):
		'''
		Try to get product when ProductType and Product categories do not match.
		We should get empty QuerySet as the output.
		'''
		prod_type = ProductType.objects.get(name='Footwear', sex='Junior')
		products = prod_type.product_class.filter(title='adidas ZX750')\
					.filter(category__in=prod_type.category.all())
		self.assertQuerysetEqual(products, 
			[], ordered=False
		)