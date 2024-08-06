from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangeForm, EditProfilePageForm, ProfilePageForm
from theblog.models import Profile, Post
from django.contrib.auth import authenticate, login


def LoginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid credentials'
    else:
        error_message = None
    return render(request, 'login.html', {'error_message': error_message})

class CreateUserProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/create_user_profile_page.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditProfilePageView(generic.UpdateView):
    model = Profile
    form_class = EditProfilePageForm
    template_name = 'registration/edit_profile_page.html'
    success_url = reverse_lazy('home')

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        blog_post = Post.objects.filter(author=page_user.user).order_by('-post_date')
        context["page_user"] = page_user
        context["blog_post"] = blog_post
        return context

class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy('password_success')
    
def password_success(request):
    return render(request, 'registration/password_success.html', {})

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')
    
    def get_object(self):
        return self.request.user
    
    

