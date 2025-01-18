from typing import Any
from django.forms import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Comment
from .forms import ProductForm, ContactForm, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse

def cateogry_views(request, cats):
    category_list = Product.objects.filter(category=cats.replace('-', ' '))
    return render(request, "categories.html", {"cats":cats.title().replace('-', ' '), "category_list":category_list}) 

def category_list_view(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'cat_list.html', {"cat_menu_list":cat_menu_list})

def LikeView(request, pk):
    post = get_object_or_404(Product, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post_detail', args=[str(pk)]))



class HomeView(generic.ListView):
    model = Product
    template_name = "index.html"
    paginate_by = 9
    cats = Category.objects.all()

    def get_context_data(self, *args ,**kwargs):
        
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data( *args ,**kwargs)
        context["cat_menu"] = cat_menu
        context["top_products"] = Product.objects.order_by("-created_at")[:8]  # Adjust as needed
        context["recent_products"] = Product.objects.order_by("-created_at")[:4] # Adjust as needed
        context['side_bar_product'] = Product.objects.order_by("-created_at")[:4]

        return context
    
class BlogEntries(generic.ListView):
    model = Product
    template_name = 'blog.html'
    paginate_by = 6
    cats = Category.objects.all()

    def get_queryset(self):
        return Product.objects.order_by('-created_at')

    def get_context_data(self, *args,**kwargs):
        cat_menu = Category.objects.all()
        context = super(BlogEntries, self).get_context_data( *args ,**kwargs)
        context['cat_menu'] = cat_menu
        context['side_bar_product'] = Product.objects.order_by("-created_at")[:4]
        return context

class ArticleDetailView(generic.DetailView):
    model = Product
    template_name = 'post-details.html'

    def get_context_data(self, *args ,**kwargs):
        stuff = get_object_or_404(Product, id=self.kwargs['pk'])
        total_likes = stuff.total_likes() # function from models 
        cat_menu = Category.objects.all()
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        context = super(ArticleDetailView, self).get_context_data( *args ,**kwargs)

        context['cat_menu'] = cat_menu
        context['side_bar_product'] = Product.objects.order_by("-created_at")[:4]
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context

def edit_product(request, pk): 
    """   """
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ProductForm(instance=product)
    return render(request, "edit.html", {"form":form, 'product':product})


def delete_product(request, pk):
    ''' The function Delete's the blog page '''
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("home")
    return render(request, "delete.html", {'product':product})

@login_required
def post_blog(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect('post_detail', pk=product.id)
    else:
        form = ProductForm()
    return render(request, 'add_blog.html', {"form":form, "errors": form.errors})

class AddCommentView(generic.CreateView):
    model = Comment
    template_name = 'post-details.html'
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.product_id = self.kwargs['pk']
        return super().form_valid(form)


def about_page(request):
    return render(request, 'about.html',{})


def contact_page(request):
    
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('contact_page')
    context = {"form":form}
    return render(request, 'contact.html', context)



def search_bar(request):
    """ this fuction is used in search-bar,
        -it looks for the parameter 'searched'
     
        then return two dict values searched and blogs   """

    if request.method == "POST":
        searched = request.POST['searched'] #looks for anything in search bar
        blogs = Product.objects.filter(name__contains=searched)  #filter out the searched product by name
        return render(request, 'search_thing.html', {'searched':searched, 'blogs':blogs})
    else:
        return render(request, 'search_thing.html', {'searched':searched})