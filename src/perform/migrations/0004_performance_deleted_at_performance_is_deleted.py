# Generated by Django 4.2.4 on 2023-09-14 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perform', '0003_remove_scene_performance_performance_scenes'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='performance',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]