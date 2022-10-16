from django.contrib import admin
from Members.models import Member, MedicalData


class MembersAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email']


class MedicalDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'member']


admin.site.register(Member, MembersAdmin)
admin.site.register(MedicalData, MedicalDataAdmin)
