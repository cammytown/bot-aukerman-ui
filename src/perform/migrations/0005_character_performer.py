# Generated by Django 4.2.4 on 2023-09-18 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perform', '0004_performance_deleted_at_performance_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='performer',
            field=models.CharField(default='gpt-large', max_length=255),
            preserve_default=False,
        ),
    ]