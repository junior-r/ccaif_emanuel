from django.urls import path
from Users.views import sign_up


urlpatterns = [
    path('signup/', sign_up, name='sign_up')
]
