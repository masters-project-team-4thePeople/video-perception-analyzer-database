# Generated by Django 3.2.18 on 2023-05-07 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos_api', '0003_auto_20230507_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videometadata',
            name='video_title',
            field=models.CharField(blank=True, default='', max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='videometadata',
            name='video_url',
            field=models.CharField(max_length=512, unique=True),
        ),
    ]