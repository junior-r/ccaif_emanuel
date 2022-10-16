from django.urls import path
from Home.views import home


urlpatterns = [
    path('', home, name='homepage')
]
