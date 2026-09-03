from django.apps import AppConfig


class PensionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pensiones'

    def ready(self):
        from django.db.models.signals import post_migrate

        def seed_fondos(sender, **kwargs):
            if sender.name == self.name:
                from .services import ensure_default_pension_funds

                ensure_default_pension_funds()

        post_migrate.connect(seed_fondos, sender=self)
