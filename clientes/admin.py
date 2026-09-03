from django.contrib import admin

from .models import Cliente, Consentimiento, TimelineEvent

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "numero_documento", "estado", "consultor", "ultima_interaccion")
    search_fields = ("nombres", "apellidos", "numero_documento", "email")
    list_filter = ("estado", "segmento", "ciudad")


admin.site.register(Consentimiento)
admin.site.register(TimelineEvent)

# Register your models here.
