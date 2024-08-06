# Generated by Django 5.0.4 on 2024-07-29 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_category_name_en_us_category_name_ru_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category_en_us',
            field=models.ManyToManyField(null=True, through='news.PostCategory', to='news.category'),
        ),
        migrations.AddField(
            model_name='post',
            name='category_ru',
            field=models.ManyToManyField(null=True, through='news.PostCategory', to='news.category'),
        ),
        migrations.AddField(
            model_name='post',
            name='created_at_en_us',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='created_at_ru',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_type_en_us',
            field=models.CharField(choices=[('article', 'Статья'), ('news', 'Новость')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_type_ru',
            field=models.CharField(choices=[('article', 'Статья'), ('news', 'Новость')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='text_ru',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_en_us',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='title_ru',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='PostCategory_en_us',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
            options={
                'verbose_name': 'post category [en-us]',
                'verbose_name_plural': 'post categorys [en-us]',
                'db_table': 'news_postcategory_en_us',
                'db_tablespace': '',
                'auto_created': False,
            },
        ),
        migrations.CreateModel(
            name='PostCategory_ru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.category')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.post')),
            ],
            options={
                'verbose_name': 'post category [ru]',
                'verbose_name_plural': 'post categorys [ru]',
                'db_table': 'news_postcategory_ru',
                'db_tablespace': '',
                'auto_created': False,
            },
        ),
    ]
