# Generated by Django 5.0 on 2024-07-30 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0012_remove_library_images_library_champ_activation'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='library',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]