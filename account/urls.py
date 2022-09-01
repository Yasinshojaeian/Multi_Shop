from django.urls import path
from . import views


app_name = 'account'
urlpatterns =[
    path('login',views.UserLogin.as_view(),name='user_login'),
    path('otplogin',views.LoginView.as_view(),name='otp_login'),
    path('check_otp',views.CheckOtpView.as_view(),name='check_otp'),
]