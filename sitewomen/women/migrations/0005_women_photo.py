# Generated by Django 5.2.3 on 2025-07-08 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0004_uploadfiles_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='women',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
