from django.shortcuts import render , redirect
from django.views import View
from .forms import CheckOtpForm, LoginForm, OtpLoginForm
from django.contrib.auth import authenticate ,login,logout
import ghasedakpack
from random import randint
from .models import Otp, User
from django.urls import reverse
from django.utils.crypto import get_random_string
from uuid import uuid4
# Create your views here.

# def user_login(request):
#     return render(request, 'account/login.html')


SMS=ghasedakpack.Ghasedak("8ccb470a1504662baa0523cc138d1c8aec749a6deed7c84278f48662af5c2f24")
class UserLogin(View):
    def get(self,request):
        form = LoginForm()
        return render(request, 'account/login.html',context={'form':form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username = cd['username'],password = cd['password'])
            if user is not None :
                login(request, user)
                return redirect('home:home')
            else :
                form.add_error("username","Invalid User Data")
        else :
            form.add_error("username","Invalid Data")
            
        return render(request, 'account/login.html',context={'form':form})
    
    
class LoginView(View):
    def get(self, request):
        form = OtpLoginForm()
        return render(request, 'account/register.html',context={'form':form})
    
    def post(self, request):
        form = OtpLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode = randint(1000,9999)
            print(randcode)
            # SMS.verification({'receptor': cd['phone'],'type': '1','template': 'randomcode','param1': randcode})
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'],code=randcode,token=token)
            return redirect(reverse('account:check_otp')+f'?token={token}')
            
        else :
            form.add_error("phone","Invalid Data")
            
        return render(request, 'account/register.html',context={'form':form})
    
class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, 'account/check_otp.html',context={'form':form})
    
    def post(self, request):
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            token = request.GET.get('token')
            if Otp.objects.filter(code=cd['code'],token = token).exists:
                otp = Otp.objects.get(token=token)
                user,is_create = User.objects.get_or_create(phone=otp.phone)
                login(request, user,backend = 'django.contrib.auth.backends.ModelBackend')
                otp.delete()
                return redirect('home:home')            
        else :
            form.add_error("phone","Invalid Data")
            
        return render(request, 'account/check_otp.html',context={'form':form})
    
    
    
def user_logout(request):
    logout(request)
    return redirect('/')