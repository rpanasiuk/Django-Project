from django.db import models
from django.core.exceptions import FieldDoesNotExist
from django.http import QueryDict
from django.db.models import Q


class ProductQuerySet(models.query.QuerySet):
	def search(self, query):
		if query:
			return self.filter(
				Q(title__icontains=query) |
				Q(price__icontains=query) |
				Q(description__icontains=query) |
				Q(category__name__icontains=query) |
				Q(product_class__name__icontains=query)
			).distinct()
		else:
			return self

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self.db)

	def search(self, query):
		return self.get_queryset().search(query)

class Product(models.Model):
	title 			= models.CharField(max_length=120)
	price 			= models.DecimalField(decimal_places=2, default=99.99, max_digits=12)
	description 	= models.TextField(max_length=500)
	category 		= models.ManyToManyField('Category', blank=True)
	product_class	= models.ForeignKey(
										'ProductType', related_name='product_class', 
										blank=False, null=True, on_delete=models.CASCADE)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)
	slug 			= models.SlugField(blank=True) 

	objects = ProductManager()

	def __str__(self):
		return self.title

class Category(models.Model):
	name 	 = models.CharField(max_length=120)
	
	class Meta:
		verbose_name_plural = 'categories'
		ordering = ['name']

	def __str__(self):
		return self.name

class ProductType(models.Model):
	name 	    = models.CharField(max_length=120)
	sex			= models.CharField(max_length=120)
	category 	= models.ManyToManyField('Category', blank=True)

	class Meta:
		unique_together = (('name', 'sex'),)

	def __str__(self):		
		cat_path = [self.name]
		k = self.sex
		
		if k:
			cat_path.append(k)
			return ' -> '.join(cat_path)
		else:
			return cat_path[0]