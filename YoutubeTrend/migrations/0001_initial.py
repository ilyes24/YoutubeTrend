# Generated by Django 2.0.4 on 2019-05-28 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.TextField(blank=True, db_column='fileName', null=True)),
                ('filelocation', models.TextField(blank=True, db_column='fileLocation', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('iduser', models.IntegerField(blank=True, db_column='idUser', null=True)),
            ],
            options={
                'db_table': 'file',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=255)),
                ('image_location', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=255)),
                ('api_key', models.CharField(max_length=255)),
                ('rank_by', models.CharField(max_length=255)),
                ('capture_in', models.IntegerField(null=True)),
                ('quality', models.CharField(max_length=40, null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operationUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_id', models.CharField(max_length=255)),
                ('video_url', models.CharField(max_length=1000)),
                ('title', models.CharField(max_length=255)),
                ('duration', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('views', models.IntegerField()),
                ('likes', models.IntegerField()),
                ('comments', models.IntegerField()),
                ('related_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videoOperation', to='YoutubeTrend.Operation')),
            ],
        ),
        migrations.CreateModel(
            name='XmlFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('file_location', models.CharField(max_length=1000)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fileVideo', to='YoutubeTrend.Video')),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imageVideo', to='YoutubeTrend.Video'),
        ),
    ]
