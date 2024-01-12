from django.urls import path
from main.views import *


urlpatterns = [
    path('', show_main, name='show_main'),
    path('json/ayat', json_ayat, name='json_ayat'), 
    path('json/surat', json_surat, name='json_surat'), 
    path('json/audio', json_audio, name='json_audio'), 
]
