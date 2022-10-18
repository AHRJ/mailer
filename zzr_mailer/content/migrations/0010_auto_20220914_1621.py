# Generated by Django 3.1.12 on 2022-09-14 16:21

from django.db import migrations, models
import django.utils.timezone
import imagekit.models.fields
import zzr_mailer.content.models.advertisement_banner


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0009_auto_20220606_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisementbanner',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to=zzr_mailer.content.models.advertisement_banner.AdvertisementBanner.content_file_name, verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='advertisementbanner',
            name='link',
            field=models.URLField(verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='advertisementbanner',
            name='title',
            field=models.CharField(default='Рекламный баннер', max_length=255, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='article',
            name='authors',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Авторы'),
        ),
        migrations.AlterField(
            model_name='article',
            name='created',
            field=models.DateField(null=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='article',
            name='doi',
            field=models.CharField(blank=True, max_length=127, null=True, verbose_name='DOI'),
        ),
        migrations.AlterField(
            model_name='article',
            name='header_photo',
            field=imagekit.models.fields.ProcessedImageField(upload_to='img/article/thumbnails', verbose_name='Заглавное изображение'),
        ),
        migrations.AlterField(
            model_name='article',
            name='issue',
            field=models.CharField(blank=True, max_length=127, null=True, verbose_name='Номер выпуска / Код спецвыпуска'),
        ),
        migrations.AlterField(
            model_name='article',
            name='link',
            field=models.URLField(verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='article',
            name='partner',
            field=models.CharField(blank=True, max_length=127, null=True, verbose_name='Партнер'),
        ),
        migrations.AlterField(
            model_name='article',
            name='rubric',
            field=models.CharField(blank=True, max_length=127, null=True, verbose_name='Рубрика'),
        ),
        migrations.AlterField(
            model_name='article',
            name='teaser',
            field=models.TextField(verbose_name='Анонс'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='article',
            name='year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Год публикации'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='cover',
            field=imagekit.models.fields.ProcessedImageField(upload_to='img/journal/thumbnails', verbose_name='Обложка'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='created',
            field=models.DateField(null=True, verbose_name='Дата размещения'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='issue',
            field=models.CharField(max_length=255, verbose_name='Номер выпуска / Код спецвыпуска'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='link',
            field=models.URLField(verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='year',
            field=models.IntegerField(blank=True, null=True, verbose_name='Год'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, upload_to='img/news/thumbnails', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='news',
            name='image_url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на изображение'),
        ),
        migrations.AlterField(
            model_name='news',
            name='link',
            field=models.URLField(verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='news',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='news',
            name='teaser',
            field=models.TextField(verbose_name='Анонс'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
    ]
