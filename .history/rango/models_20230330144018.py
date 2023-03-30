from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    NAME_MAX_LENGTH = 128
    
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name
    
class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH)
    url = models.URLField()
    views = models.IntegerField(default=0)
    last_visit = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.title
    
class MyUser(AbstractUser):
    
    username = models.CharField(max_length=25, primary_key=True)
    age = models.IntegerField(blank=True, null=True)
    occupation = models.CharField(max_length=12, blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
class UserProfile(models.Model):
    
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    
    def image_path(self, filename):
        print("profile_images/%s/%s" % (self.user.username, filename))
        return "profile_images/%s/%s" % (self.user.username, filename)
    
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to=image_path, blank=True)
    
    liked_categories = models.ManyToManyField(Category)
    
    def __str__(self):
        return self.user.username
