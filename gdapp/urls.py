from django.urls import path


from gdapp.views import home, realtor_register,client_realtor_info,user_login,user_logout,realtor_dashboard,contactus,realtor_profile

app_name = 'gdapp'
urlpatterns =[
    path('',home, name='home'),
    path('contactus',contactus, name='home'),
    path('realtor',realtor_register, name='realtor_register'),
    path('realtor/profile/<str:referral_code>',realtor_profile, name='realtor_profile'),
    path('realtor/<str:referral_code>',realtor_register, name='realtor_referral_register'),
    path('client_confirmation/<str:referral_code>',client_realtor_info, name='client_realtor_info'),
    path('user_login',user_login, name='user_login'),
    path('logout',user_logout, name='user_logout'),
    path('dashboard/<str:realtor>',realtor_dashboard, name='realtor_dashboard'),

]



