# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APILog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activity', models.TextField(null=True)),
                ('syncd', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Counties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('AdministrativeUnitCode', models.CharField(max_length=50, null=True, blank=True)),
                ('ParentCode', models.CharField(max_length=50, null=True, blank=True)),
                ('AdministrativeUnitName', models.CharField(max_length=50, null=True, blank=True)),
                ('OrderOfEntry', models.CharField(max_length=50, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('second_name', models.CharField(max_length=50, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('date_of_birth', models.DateTimeField(null=True, verbose_name='DOB')),
                ('email', models.EmailField(max_length=70, blank=True)),
                ('address', models.CharField(max_length=50, blank=True)),
                ('national_id', models.CharField(max_length=50, blank=True)),
                ('acc_number', models.CharField(max_length=50)),
                ('pin', models.IntegerField(default=2222)),
                ('profession', models.CharField(max_length=50, blank=True)),
                ('cluster', models.CharField(max_length=50, blank=True)),
                ('center', models.CharField(max_length=50, blank=True)),
                ('town', models.CharField(max_length=50, blank=True)),
                ('county', models.CharField(max_length=50, blank=True)),
                ('country', models.CharField(default=b'Kenya', max_length=50, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('bal_amount', models.DecimalField(default=0.0, max_digits=19, decimal_places=2)),
                ('date_added', models.DateTimeField(verbose_name='Date Added')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
