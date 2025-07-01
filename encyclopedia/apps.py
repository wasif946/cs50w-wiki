from django.apps import AppConfig

class EncyclopediaConfig(AppConfig):
    # Set the default_auto_field for models in this app.
    # This helps address the models.W042 warning specifically for this app,
    # though it's also handled by DEFAULT_AUTO_FIELD in settings.py globally.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'encyclopedia'
    
    def ready(self):
        # You can add any app-specific initialization code here.
        # For example, importing signals, if you have any.
        pass