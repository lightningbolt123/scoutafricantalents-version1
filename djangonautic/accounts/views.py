from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomUserChangeForm, UserGroupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .utils import generate_token
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def account_types(request):
    return render(request, 'account-type.html')

def signup(request):
    User = get_user_model()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            newusername = form.cleaned_data['username']
            firstname = form.cleaned_data['first_name']
            lastname = form.cleaned_data['last_name']
            to_mail = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            try:
                query_set = User.objects.get(email=to_mail)
            except ObjectDoesNotExist:
                query_set = None
            if query_set is not None:
                user.username = newusername
                user.first_name = firstname
                user.last_name = lastname
                user.email = to_mail
                user.is_active = False
                user.set_password(password)
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('accounts/acc_active_email.html', {
                    'user':user,
                    'domain':current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':generate_token.make_token(user),
                })
                email = EmailMessage(
                            mail_subject, 
                            message, 
                            to=[to_mail]
                )
                email.send()
                return HttpResponse('Please visit the link sent to your email to activate your account')
            else:
                current_site = get_current_site(request)
                mail_subject = 'Signup was unsuccessful'
                message = render_to_string('accounts/unable_to_create_acc.html', {
                    'user':user,
                    'domain':current_site.domain
                })
                email = EmailMessage(
                            mail_subject, 
                            message, 
                            to=[to_mail]
                )
                email.send()
                return HttpResponse('Subscribe to a plan before signing up')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup-form.html', {'form':form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as identifier:
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        messages.add_message(request, messages.INFO, 'account activated successfully')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('activity-log')
    else:
        form = AuthenticationForm()
    return render(request, 'application/login.html', {'form':form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')

def forgot_password(request):
    return render(request, 'application/forgot-password.html')


