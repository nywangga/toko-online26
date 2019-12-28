# Generated by Django 2.2 on 2019-12-12 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_address_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=7)),
                ('amount', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='courier',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Courier'),
        ),
    ]
