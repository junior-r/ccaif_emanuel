from django.contrib import admin
from Users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'picture_profile', 'first_name', 'last_name', 'date_joined', 'is_superuser', 'is_staff']


admin.site.register(User, UserAdmin)
