# Generated by Django 2.2 on 2019-12-12 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20191212_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(default='087882320678', max_length=14),
            preserve_default=False,
        ),
    ]
