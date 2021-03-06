# Generated by Django 4.0.1 on 2022-01-18 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Social_Network', models.CharField(max_length=255)),
                ('Post_Id', models.CharField(max_length=1000)),
                ('Key_word', models.CharField(max_length=255)),
                ('Names', models.CharField(max_length=255)),
                ('Link_post', models.CharField(max_length=5000)),
                ('post', models.CharField(max_length=400)),
                ('comment', models.CharField(max_length=5000)),
                ('device', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('Job_title', models.CharField(max_length=255)),
                ('time', models.CharField(max_length=255)),
                ('user', models.CharField(max_length=255)),
                ('Note', models.CharField(max_length=255)),
                ('published', models.BooleanField(default=False)),
            ],
        ),
    ]
