from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="media/profile_pic")
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    website_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    instagram_url = models.URLField(max_length=255, null=True, blank=True)
    pinterest_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)
   

    def __str__(self):
        return str(self.user) 
    
    def get_absolute_url(self):
        return reverse('home')



class Category(models.Model):
    name =  models.CharField(max_length=255)
    image = models.ImageField( upload_to='category/')


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('home')


class Product(models.Model):
    author = models.ForeignKey(User ,on_delete=models.CASCADE )
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    # description = models.TextField()
    category = models.CharField(max_length=255, default="uncategorized")
    image = models.ImageField( upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="blog_post")

    def __str__(self):
        return self.name + ' | ' + str(self.author)
    
    def total_likes(self):
        return self.likes.count()

    def edit(self, name, description, image):
        self.name = name
        self.description = description
        self.image =image
        self.save()

    def short_description(self):
        word = self.description.split()  #spilt the word into list 
        if len(word) > 50:  # if word are greater than 50 then 
            return " ".join(word[:30]) + "..."
        else:
            return self.description
        


class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.subject + ' ' +self.email
    

class Comment(models.Model):
    post = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)