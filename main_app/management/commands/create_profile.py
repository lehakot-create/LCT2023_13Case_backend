from django.core.management.base import BaseCommand

from ...models import Profile, Idea, Stack


class Command(BaseCommand):
    help = "This command populates the database"

    def handle(self, *args, **kwargs):
        try:
            profile = Profile.objects.get(id=1)
            profile.full_name = "Дмитрий Петрович"
            profile.dateofbirth = "01.01.1990"
            profile.country = 'Россия'
            profile.citizenship = 'Россия'
            profile.gender = 'male'
            profile.profession = 'Backend'
            profile.stack = 'Python Django'
            profile.save()

            idea = Idea.objects.create(
                author=profile,
                name="Интерактивная карта ВДНХ",
                description="Краткое описание идеи для отображения в карточке проекта",
            )
            stack = Stack.objects.get(id=13)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=5)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=8)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=26)
            idea.stack.add(stack)

            idea = Idea.objects.create(
                author=profile,
                name="Сервис мониторинга состояния заявок в сфере ЖКХ",
                description="Краткое описание идеи для отображения в карточке проекта",
            )
            stack = Stack.objects.get(id=13)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=5)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=8)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=26)
            idea.stack.add(stack)

            idea = Idea.objects.create(
                author=profile,
                name="Рекомендательный сервис по выявлению перспективных производств",
                description="Краткое описание идеи для отображения в карточке проекта",
            )
            stack = Stack.objects.get(id=13)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=5)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=8)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=26)
            idea.stack.add(stack)

            idea = Idea.objects.create(
                author=profile,
                name="Интерактивная карта для формирования границ территорий Москвы",
                description="Краткое описание идеи для отображения в карточке проекта",
            )
            stack = Stack.objects.get(id=13)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=5)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=8)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=26)
            idea.stack.add(stack)

            idea = Idea.objects.create(
                author=profile,
                name="Сервис автоматического разбора и структурирования градостроительных планов",
                description="Краткое описание идеи для отображения в карточке проекта",
            )
            stack = Stack.objects.get(id=1)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=17)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=27)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=28)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=8)
            idea.stack.add(stack)

            idea = Idea.objects.create(
                author=profile,
                name="Сервис формирования задач для москвичей по контролю работы подрядчиков",
                description="Краткое описание идеи для отображения в карточке проекта",
            )
            stack = Stack.objects.get(id=1)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=17)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=27)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=28)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=8)
            idea.stack.add(stack)

            idea = Idea.objects.create(
                author=profile,
                name="Веб-платформа для разметки медицинских изображений",
                description="Краткое описание идеи для отображения в карточке проекта",
            )
            stack = Stack.objects.get(id=1)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=17)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=27)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=28)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=8)
            idea.stack.add(stack)

            idea = Idea.objects.create(
                author=profile,
                name="Рекомендательный сервис для определения оптимальных мест размещения постаматов",
                description="Краткое описание идеи для отображения в карточке проекта",
            )
            stack = Stack.objects.get(id=1)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=17)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=27)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=28)
            idea.stack.add(stack)
            stack = Stack.objects.get(id=8)
            idea.stack.add(stack)

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
