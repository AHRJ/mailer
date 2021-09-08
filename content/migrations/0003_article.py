# Generated by Django 3.1.12 on 2021-09-08 19:43

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20210907_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.CharField(max_length=63, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('authors', models.CharField(blank=True, max_length=255, null=True)),
                ('teaser', models.TextField()),
                ('link', models.URLField()),
                ('header_photo', imagekit.models.fields.ProcessedImageField(upload_to='img/article/thumbnails')),
                ('header_photo_url', models.URLField(blank=True, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('issue', models.CharField(blank=True, max_length=127, null=True)),
                ('rubric', models.CharField(blank=True, max_length=127, null=True)),
                ('doi', models.CharField(blank=True, max_length=127, null=True)),
                ('partner', models.CharField(blank=True, max_length=127, null=True)),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]