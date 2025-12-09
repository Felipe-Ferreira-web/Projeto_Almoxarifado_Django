from django.apps import AppConfig


class StorageConfig(AppConfig):
    """
    Configuration class for the 'storage' application.

    This class provides configuration settings that Django loads when the application
    is started, allowing for customization of application-specific behavior.

    Attributes:
    -----------
    default_auto_field : str
        Specifies the type of primary key to be used for models in this app.
        'django.db.models.BigAutoField' ensures a 64-bit integer auto-incrementing field.
    name : str
        The short Python import path for the application (must be unique).
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "storage"
