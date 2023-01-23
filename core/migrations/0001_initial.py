# Generated by Django 4.1 on 2023-01-20 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.TextField(blank=True)),
                ('birthday', models.DateField(null=True, verbose_name='Birthday')),
                ('country', django_countries.fields.CountryField(max_length=2, null=True, verbose_name='Country')),
                ('city', models.CharField(max_length=100, verbose_name='City in English')),
                ('affiliation', models.CharField(max_length=100, verbose_name='Name of your organization in English')),
                ('photo', models.ImageField(blank=True, default='https://static.productionready.io/images/smiley-cyrus.jpg', max_length=100000, null=True, upload_to='media/')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
