from django.test import TestCase
from rango.models import Category

# Create your tests here.
class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        category = Category(name='test', views=-1, likes=0)
        category.save()
        
        self.assertEqual((category.views >= 0), True)