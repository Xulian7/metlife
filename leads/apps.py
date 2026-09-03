from django.apps import AppConfig


class LeadsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leads'

    def ready(self):
        from django.db.models.signals import post_migrate

        def seed_pipeline(sender, **kwargs):
            if sender.name == self.name:
                from .services import ensure_default_pipeline

                ensure_default_pipeline()

        post_migrate.connect(seed_pipeline, sender=self)
