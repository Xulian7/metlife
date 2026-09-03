from django.contrib import admin

from .models import Lead, LeadStageHistory, PipelineStage, Seguimiento

admin.site.register(PipelineStage)
admin.site.register(Lead)
admin.site.register(LeadStageHistory)
admin.site.register(Seguimiento)

# Register your models here.
