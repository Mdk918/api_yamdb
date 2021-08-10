# Generated by Django 2.2.16 on 2021-08-10 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20210810_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'юзер'), ('moderator', 'модератор'), ('admin', 'админ')], default='user', max_length=50, verbose_name='Роль пользователя'),
        ),
    ]
