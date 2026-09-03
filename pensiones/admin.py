from django.contrib import admin

from .models import FondoPensiones, NormativaPensional, PensionRule

admin.site.register(FondoPensiones)
admin.site.register(NormativaPensional)
admin.site.register(PensionRule)

# Register your models here.
