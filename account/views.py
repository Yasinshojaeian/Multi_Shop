from django.shortcuts import render , redirect
from django.views import View
from .forms import LoginForm
from django.contrib.auth import authenticate ,login

# Create your views here.

# def user_login(request):
#     return render(request, 'account/login.html')
class UserLogin(View):
    def get(self,request):
        form = LoginForm()
        return render(request, 'account/login.html',context={'form':form})
    
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username = cd['phone'],password = cd['password'])
            if user is not None :
                login(request, user)
                return redirect('home:home')
            else :
                form.add_error("phone","Invalid User Data")
        else :
            form.add_error("phone","Invalid Data")
            
        return render(request, 'account/login.html',context={'form':form})