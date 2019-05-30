from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from YoutubeTrend import views

urlpatterns = [
    path('digIn', csrf_exempt(views.dig_it), name='DigIn'),
    path('savefile', csrf_exempt(views.saveFile), name='saveFile')

]
