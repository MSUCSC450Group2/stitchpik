# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('image_manipulation', '0002_auto_20150324_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='imgFile',
            field=models.ImageField(upload_to='static/images/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
