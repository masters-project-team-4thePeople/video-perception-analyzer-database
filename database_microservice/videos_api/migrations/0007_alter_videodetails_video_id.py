# Generated by Django 3.2.18 on 2023-05-07 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos_api', '0006_alter_videodetails_video_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videodetails',
            name='video_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='videos_api.videometadata'),
        ),
    ]
