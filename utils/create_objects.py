import os
import sys
from datetime import datetime
from pathlib import Path
import random
from list_itens import objects
import faker
from faker.providers import BaseProvider

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent
NUMBER_OF_OBJECTS = 1000

sys.path.append(str(DJANGO_BASE_DIR))
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"

django.setup()

settings.USE_TZ = False

if __name__ == "__main__":

    from storage.models import Item

    Item.objects.all().delete()

    fake = faker.Faker("pt_BR")

    django_storage = []

    class StorageProvider(BaseProvider):
        def random_object_name(self):
            return self.random_element(objects)

        def random_storage_location(self):
            local = ["Armazem", "Pátio 1", "Pátio 2", "Pátio 3"]
            return self.random_element(local)

    fake.add_provider(StorageProvider)

    for _ in range(NUMBER_OF_OBJECTS):
        object = fake.random_object_name()
        description = fake.text(max_nb_chars=70)
        quantity = random.randint(1, 10)
        storage_location = fake.random_storage_location()
        is_available = bool(random.getrandbits(1))
        created_date = datetime = fake.date_this_year()
        django_storage.append(
            Item(
                object=object,
                description=description,
                quantity=quantity,
                storage_location=storage_location,
                is_available=is_available,
                created_date=created_date,
            )
        )

    if len(django_storage) > 0:
        Item.objects.bulk_create(django_storage)
