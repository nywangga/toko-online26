# Generated by Django 2.2 on 2019-12-11 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_coupon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='coupon',
            new_name='name',
        ),
        migrations.AddField(
            model_name='order',
            name='coup',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Coupon'),
        ),
    ]
