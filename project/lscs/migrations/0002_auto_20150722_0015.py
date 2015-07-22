# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lscs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChecklistItemGroup',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='group',
            field=models.ForeignKey(related_name='checklistItems', default=1, to='lscs.ChecklistItemGroup'),
            preserve_default=False,
        ),
    ]
