# Generated by Django 5.0 on 2024-07-31 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0018_alter_livre_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='libraries/'),
        ),
    ]