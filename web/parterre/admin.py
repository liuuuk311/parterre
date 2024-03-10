from django.contrib import admin
from csvexport.actions import csvexport


# Register Contact Model here
from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    actions = [csvexport]

admin.site.register(Contact, ContactAdmin)