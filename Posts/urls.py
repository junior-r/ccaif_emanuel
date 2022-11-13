from django.urls import path
from Posts.views import events, create_event, register_form_event


urlpatterns = [
    path('events/', events, name='events'),
    path('create_event/<int:user_id>/', create_event, name='create_event'),
    path('register_event/<int:event_id>/', register_form_event, name='register_event'),
]
