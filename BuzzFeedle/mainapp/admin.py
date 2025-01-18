from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Category, Profile, Comment
# Register your models here.


admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Comment)
