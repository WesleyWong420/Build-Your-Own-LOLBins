# Generated by Django 4.1.4 on 2022-12-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_glob_created_glob_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='status',
            field=models.CharField(choices=[('STOPPED', 'STOPPED'), ('COMPLETED', 'COMPLETED'), ('RUNNING', 'RUNNING'), ('ERROR', 'ERROR')], default='STOPPED', max_length=15),
        ),
    ]
