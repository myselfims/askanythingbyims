# Generated by Django 4.1 on 2022-11-23 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll_app', '0004_question_allow_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]