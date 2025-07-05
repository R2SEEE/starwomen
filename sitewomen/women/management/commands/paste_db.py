import random
from django.utils.text import slugify
from django.core.management.base import BaseCommand

from women.models import Women, Category


class Command(BaseCommand):
    help = 'Заполняет базу данных SQLite тестовыми данными'

    def handle(self, *args, **kwargs):
        first_names = [
            'Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia',
            'Charlotte', 'Mia', 'Amelia', 'Harper', 'Evelyn'
        ]

        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones',
            'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'
        ]

        contents = [
            "Известная актриса театра и кино.",
            "Выдающаяся певица современности.",
            "Талантливая художница и скульптор.",
            "Знаменитая писательница и поэтесса.",
            "Известный политический деятель.",
            "Выдающийся ученый в своей области.",
            "Прославленная спортсменка.",
            "Легендарная балерина.",
            "Знаменитая модель и актриса.",
            "Известный общественный деятель."
        ]

        for i in range(1, 101):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            title = f"{first_name} {last_name}"
            slug = slugify(f"{first_name}-{last_name}-{i}")
            content = random.choice(contents)

            Women.objects.create(
                title=title,
                slug=slug,
                content=content,
                is_published=random.choice([Women.Status.DRAFT, Women.Status.PUBLISHED]),
                cat_id=random.choice([1, 2])
            )

        self.stdout.write(self.style.SUCCESS('Успешно создано 100 записей в таблице Woman'))
