from django.apps import AppConfig


class CategoryAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'category_app'

    def ready(self):
        import category_app.signals
