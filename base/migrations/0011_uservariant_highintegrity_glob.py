# Generated by Django 4.1.1 on 2022-11-28 02:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_scan_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='uservariant',
            name='highIntegrity',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='No', max_length=3, verbose_name='High Integrity Process'),
        ),
        migrations.CreateModel(
            name='Glob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=200)),
                ('Variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.variant')),
            ],
            options={
                'verbose_name': 'Globfuscation',
            },
        ),
    ]
