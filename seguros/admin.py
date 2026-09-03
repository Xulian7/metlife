from django.contrib import admin

from .models import CoberturaExistente, DiagnosticoProteccion

admin.site.register(DiagnosticoProteccion)
admin.site.register(CoberturaExistente)

# Register your models here.
