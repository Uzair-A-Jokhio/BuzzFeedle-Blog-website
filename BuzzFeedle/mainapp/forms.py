from django import forms
from .models import Product, Contact, Category, Comment


# this snippet of code to get catergory fro Category model 
choice = Category.objects.all().values_list('name','name')
choice_list = [i for i in choice]

#this is a form for blog 
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['author','name', 'description','category', "image"]

        widgets = {
            'author':forms.TextInput( attrs={'class': 'form-control', 'value':'', 'id':'user_name', 'type':'hidden'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category':forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'subject', 'message']

        widgets ={
            "full_name": forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your full Name'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email address'}),
            'subject': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter the subject'}),
            'message': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter the message'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets ={
            "name": forms.TextInput(attrs={ 'placeholder':'Enter your Name'}),
            'body': forms.Textarea(attrs={'placeholder':'Enter the message'}),
        }

