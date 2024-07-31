# Generated by Django 5.0 on 2024-07-31 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0013_library_is_active_library_is_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='library',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='livre',
            name='status',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
