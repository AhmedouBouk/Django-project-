# Generated by Django 5.0 on 2024-07-31 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0015_alter_livre_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livre',
            name='status',
            field=models.CharField(default='disponible', max_length=50),
        ),
    ]