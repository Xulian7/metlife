from django.apps import AppConfig


class ClientesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientes'

    def ready(self):
        from django.db.models.signals import post_migrate

        def seed_states(sender, **kwargs):
            if sender.name == self.name:
                from .services import ensure_default_client_states

                ensure_default_client_states()

        post_migrate.connect(seed_states, sender=self)
