from django.contrib import admin
from .models import User, PersonProfile, CompanyProfile, Fields

admin.site.register(User)
admin.site.register(Fields)
admin.site.register(PersonProfile)
admin.site.register(CompanyProfile)
