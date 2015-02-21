# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20150218_0319'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Login',
            new_name='LoginOld',
        ),
    ]
