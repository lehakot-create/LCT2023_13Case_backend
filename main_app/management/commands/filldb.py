from django.core.management.base import BaseCommand

from .profession import value
from ...models import Profession


class Command(BaseCommand):
    help = "This command populates the database"

    def handle(self, *args, **kwargs):
        for val in value:
            try:
                Profession.objects.create(name=val)
            except BaseException as e:
                print(e)
        self.stdout.write(self.style.SUCCESS('Данные успешно записаны в базу данных'))
