# Generated by Django 4.2.4 on 2023-08-21 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('kind', models.CharField(choices=[('rooms', 'Rooms'), ('experiences', 'Experiences')], max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
