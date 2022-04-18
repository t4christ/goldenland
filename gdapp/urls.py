from django.urls import path


from gdapp.views import home, realtor_register,client_realtor_info,user_login,user_logout,realtor_dashboard

app_name = 'gdapp'
urlpatterns =[
    path('',home, name='home'),
    path('realtor',realtor_register, name='realtor_register'),
    path('client_confirmation/<str:referral_code>',client_realtor_info, name='client_realtor_info'),
    path('user_login',user_login, name='user_login'),
    path('logout',user_logout, name='user_logout'),
    path('dashboard/<str:realtor>',realtor_dashboard, name='realtor_dashboard'),

]



