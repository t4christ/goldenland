from django.urls import path


from gdapp.views import home, realtor_register

app_name = 'gdapp'
urlpatterns =[
    path('',home, name='home'),
    path('realtor',realtor_register, name='realtor_register'),
]



