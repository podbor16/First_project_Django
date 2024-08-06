# Generated by Django 5.0.4 on 2024-07-29 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_category_name_mymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_en_us',
            field=models.CharField(help_text='имя категории', max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(help_text='имя категории', max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='name_en_us',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mymodel',
            name='name_ru',
            field=models.CharField(max_length=100, null=True),
        ),
    ]