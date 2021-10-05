# Generated by Django 3.2.7 on 2021-09-15 04:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropexplorer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crop',
            old_name='crop_number',
            new_name='heat_tolerance',
        ),
        migrations.AddField(
            model_name='crop',
            name='cover_crop_group',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crop',
            name='crop_description',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crop',
            name='crop_scientific_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crop',
            name='family_common_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crop',
            name='family_scientific_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crop',
            name='shade_tolerance',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='crop',
            name='zone_inclusion',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]