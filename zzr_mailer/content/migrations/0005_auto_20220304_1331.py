# Generated by Django 3.1.12 on 2022-03-04 13:31

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_advertisement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='img/news/thumbnails'),
        ),
    ]
