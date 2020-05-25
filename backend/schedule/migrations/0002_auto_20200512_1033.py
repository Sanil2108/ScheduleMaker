# Generated by Django 3.0.5 on 2020-05-12 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterUniqueTogether(
            name='schedule',
            unique_together={('owner', 'date')},
        ),
    ]
