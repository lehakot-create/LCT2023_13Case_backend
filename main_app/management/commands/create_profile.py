from django.core.management.base import BaseCommand

from .profession import value
from ...models import Profile


class Command(BaseCommand):
    help = "This command populates the database"

    def handle(self, *args, **kwargs):
        try:
            profile = Profile.objects.get(id=1)
            profile.full_name = "Иван Иваныч Иванов"
            profile.dateofbirth = "01.01.1990"
            profile.country = 'Россия'
            profile.citizenship = 'Россия'
            profile.gender = 'male'
            profile.profession = 'Backend'
            profile.stack = 'Python Django'
            profile.save()

            profile = Profile.objects.get(id=2)
            profile.full_name = "Петр Петрович Петров"
            profile.dateofbirth = "01.01.1990"
            profile.country = 'Россия'
            profile.citizenship = 'Россия'
            profile.gender = 'male'
            profile.profession = 'Frontend'
            profile.stack = 'JavaScript React'
            profile.save()

            profile = Profile.objects.get(id=3)
            profile.full_name = "Сидр Сидорович Сидоров"
            profile.dateofbirth = "01.01.1990"
            profile.country = 'Россия'
            profile.citizenship = 'Россия'
            profile.gender = 'male'
            profile.profession = 'Просто грузчик'
            profile.stack = 'Гружу Нагружаю'
            profile.save()
        except BaseException as e:
            print(e)
        self.stdout.write(self.style.SUCCESS('Данные успешно записаны в базу данных'))
