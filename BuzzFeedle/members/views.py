from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from .forms import UserSignupForm, EditProfileForm, PasswordChangingForm, CreateProfilePageForm, EditUserProfilePageForm
from django.views import generic
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from mainapp.models import Profile
# Create your views here.

class CreateProfilePageView(generic.CreateView):
    model = Profile
    template_name = 'authen/create_user_profile_page.html'
    form_class = CreateProfilePageForm

    def form_vaild(self, form):
        form.instance.user = self.request.user
        return super().form_vaild(form)

class ShowProfilePageView(generic.DetailView):
    model = Profile
    template_name = 'authen/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context
    
       
class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = "authen/edit_user_profile.html"
    form_class = EditUserProfilePageForm
    # fields = ['bio', 'profile_pic', 'website_url','facebook_url','twitter_url','instagram_url','pinterest_url','linkedin_url']
    success_url = reverse_lazy('home')

   

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    # form_class = PasswordChangeForm
    template_name = 'authen/change_password.html'
    success_url = reverse_lazy('password_success')

def password_sucess(request):
    return render(request, 'authen/password_sucess.html',{})

class UserEditView(generic.UpdateView):
    form_class =EditProfileForm
    template_name = 'authen/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

def login_user(request):
    if request.method =="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f"Welcome {username} ")
            return redirect('home')
        else:
            messages.info(request, f"Username and password not valid or Account dosen't exists!!! ")
            return redirect('login')
    
    return render(request, 'authen/login.html', {})

def logout_user(request):
    logout(request)
    messages.info(request, "You have been Logged OUT")
    return redirect('home')

def signup_user(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()   
            messages.success(request, "Your account has been created! Now you can Login")
            return redirect('login')
        else:
            messages.error(request, "Oops! Something went wrong. Please correct the errors below.")
    else:
        form = UserSignupForm()
    return render(request, 'authen/signup.html', {'form':form})


def welcome_mail(username, email):
    htmly = get_template('authen/email.html')
    d = { 'username': username }
    subject, from_email, to = 'welcome', 'your_email@gmail.com', email
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()