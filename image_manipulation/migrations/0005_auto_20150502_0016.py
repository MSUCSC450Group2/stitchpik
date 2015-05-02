# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_manipulation', '0004_auto_20150407_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='imgFile',
            field=models.ImageField(upload_to='image/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
