# Generated by Django 2.2.3 on 2019-07-30 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190703_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatars/default-avatar.png', upload_to='avatars', verbose_name='profile picture'),
        ),
    ]
