import random
import string
from django.utils.text import slugify

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance, new_slug=None):
	if new_slug is None:
		slug = new_slug
	else:
		slug = slugify(instance.title)

	prod_class = instance.__class__
	check_slug = prod_class.objects.filter(slug=slug).exists()
	if check_slug:
		new_slug = '{}-{}'.format(slug, random_string_generator(size=4))
		return unique_slug_generator(instance, new_slug=new_slug)
	return slug