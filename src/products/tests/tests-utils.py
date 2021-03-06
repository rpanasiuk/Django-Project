from django.test import TestCase

from products.utils import unique_slug_generator, random_string_generator
from products.models import Product


class SlugTestCase(TestCase):

	def setUp(self):
		instance = Product(
			title='New Air Max',
			price = 200,
			description='Delivery takes place 4 days.'
		)
		instance.save()

	def test_unique_slug_generator(self):
		instance = Product.objects.get(title='New Air Max')
		slug = unique_slug_generator(instance)
		self.assertEquals(slug, 'new-air-max')