# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublishedConfession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document', models.TextField()),
                ('submitted_date', models.TimeField(auto_now_add=True, null=True)),
                ('classify_score', models.FloatField(null=True, blank=True)),
                ('published_id', models.IntegerField(default=0)),
                ('published_date', models.TimeField(auto_now_add=True)),
                ('confession_url', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
