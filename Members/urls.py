from django.urls import path
from Members.views import create, view_members, view_member, create_medical_data, create_academic_data, edit_member, \
    edit_medical_data, edit_academic_data


urlpatterns = [
    path('', view_members, name='members'),
    path('create/', create, name='create_member'),
    path('view/<int:id>/<str:full_name>/', view_member, name='view_member'),
    path('create_medical_data/<int:member_id>/', create_medical_data, name='create_medical_data'),
    path('create_academic_data/<int:member_id>/', create_academic_data, name='create_academic_data'),
    path('edit_member/<int:member_id>/<str:full_name>/', edit_member, name='edit_member'),
    path('edit_medical_data/<int:member_id>/<str:full_name>/', edit_medical_data, name='edit_medical_data'),
    path('edit_academic_data/<int:member_id>/<str:full_name>/', edit_academic_data, name='edit_academic_data'),
]
