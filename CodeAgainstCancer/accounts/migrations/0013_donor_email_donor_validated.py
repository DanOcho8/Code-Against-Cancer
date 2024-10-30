# Generated by Django 4.2.16 on 2024-12-05 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_donor_amount_alter_donor_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='donor',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='donor',
            name='validated',
            field=models.BooleanField(default=False),
        ),
    ]