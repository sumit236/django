# Generated by Django 2.0.2 on 2020-03-27 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='url',
            field=models.TextField(),
        ),
    ]
