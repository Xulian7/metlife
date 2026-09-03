from django.contrib import admin

from .models import Cliente, ClienteEstado, ClienteEstadoHistory, Consentimiento, SeguimientoCliente, TimelineEvent

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre_completo", "numero_documento", "estado_relacion", "fondo_pensiones", "consultor", "ultima_interaccion")
    search_fields = ("nombres", "apellidos", "numero_documento", "email")
    list_filter = ("estado", "segmento", "ciudad")


admin.site.register(Consentimiento)
admin.site.register(ClienteEstado)
admin.site.register(ClienteEstadoHistory)
admin.site.register(SeguimientoCliente)
admin.site.register(TimelineEvent)

# Register your models here.
