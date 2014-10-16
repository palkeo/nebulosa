# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rss', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='concepts',
            field=models.ManyToManyField(related_name='entries', to='rss.Concept'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='url',
            field=models.TextField(unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=None,
        ),
    ]
