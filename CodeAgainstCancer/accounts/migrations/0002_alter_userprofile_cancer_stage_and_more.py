# Generated by Django 5.0.3 on 2024-08-23 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cancer_stage',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cancer_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='date_diagnosed',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True),
        ),
    ]