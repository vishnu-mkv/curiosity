# Generated by Django 3.2.3 on 2021-09-30 05:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0004_submission_date_submitted'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='summary',
            field=models.CharField(default='hello', max_length=1000),
            preserve_default=False,
        ),
    ]