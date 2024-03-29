# Generated by Django 3.2.16 on 2024-03-08 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0002_rating'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'get_latest_by': 'created', 'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='ride',
            options={'get_latest_by': 'created', 'ordering': ['-created']},
        ),
        migrations.AlterField(
            model_name='rating',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Fecha y hora en la que se creo el objeto', verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='modified',
            field=models.DateTimeField(auto_now=True, help_text='Fecha y hora en la que el objeto fue modificado por última vez', verbose_name='modified at'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Fecha y hora en la que se creo el objeto', verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='ride',
            name='modified',
            field=models.DateTimeField(auto_now=True, help_text='Fecha y hora en la que el objeto fue modificado por última vez', verbose_name='modified at'),
        ),
    ]
