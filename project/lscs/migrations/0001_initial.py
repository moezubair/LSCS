# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('file_number', models.CharField(max_length=30)),
                ('land_district', models.CharField(max_length=50)),
                ('latitude', models.DecimalField(max_digits=8, decimal_places=3)),
                ('longitude', models.DecimalField(max_digits=8, decimal_places=3)),
                ('status', models.IntegerField(choices=[(1, 'In Progress'), (2, 'Under Review'), (3, 'Completed')])),
                ('assigned_to', models.ForeignKey(related_name='checklistsAssigned', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(related_name='checklistsCreated', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChecklistComment',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('text', models.TextField()),
                ('checklist', models.ForeignKey(related_name='comments', to='lscs.Checklist')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistItem',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistItemSelection',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('selection', models.IntegerField(choices=[(1, 'Unanswered'), (2, 'Yes'), (3, 'N/A')])),
                ('checklist', models.ForeignKey(related_name='itemSelections', to='lscs.Checklist')),
                ('checklistItem', models.ForeignKey(to='lscs.ChecklistItem')),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
