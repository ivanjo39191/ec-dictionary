# Generated by Django 3.2.5 on 2022-12-18 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dict_id', models.CharField(max_length=20, verbose_name='Order Id')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
            ],
            options={
                'verbose_name': '英漢單字本',
                'verbose_name_plural': '英漢單字本',
            },
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_en', models.CharField(max_length=255, verbose_name='English Name')),
                ('name_zh', models.CharField(max_length=255, verbose_name='Chinese Name')),
                ('kk', models.CharField(blank=True, max_length=255, null=True, verbose_name='讀音')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
            ],
            options={
                'verbose_name': '英漢單字',
                'verbose_name_plural': '英漢單字',
            },
        ),
        migrations.CreateModel(
            name='RelationalDictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecdict.dictionary', verbose_name='單字本')),
                ('vocabulary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecdict.vocabulary')),
            ],
        ),
        migrations.CreateModel(
            name='Expatiation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_of_speech', models.CharField(max_length=255, verbose_name='詞性')),
                ('name_zh', models.CharField(max_length=255, verbose_name='釋義')),
                ('example_sentences', models.TextField(blank=True, max_length=1000, null=True, verbose_name='例句')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modified Date')),
                ('vocabulary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expatiation_set', to='ecdict.vocabulary')),
            ],
            options={
                'verbose_name': '釋義',
                'verbose_name_plural': '釋義',
            },
        ),
        migrations.AddField(
            model_name='dictionary',
            name='vocabulary',
            field=models.ManyToManyField(blank=True, related_name='dictionary_set', through='ecdict.RelationalDictionary', to='ecdict.Vocabulary', verbose_name='Vocabulary'),
        ),
    ]
