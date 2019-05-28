from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as loginview

from users import views
from users.forms import LoginForm

urlpatterns = [
    path('login/', loginview.LoginView.as_view(), {'authentication_form': LoginForm}),
    path('logoutnow/', views.logoutnow, name='logoutnow'),
    url(r'^logout/$',views.LogoutView.as_view(),name='logout'),
    path('', views.home, name='Home'),

]