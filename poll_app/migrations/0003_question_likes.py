# Generated by Django 4.1 on 2022-11-12 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll_app', '0002_question_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]