# Generated by Django 2.2.28 on 2022-08-05 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysfiles',
            name='creator',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='sysfiles',
            name='monitor',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='monitor.Monitor', verbose_name='关联服务器监控信息'),
        ),
        migrations.AddField(
            model_name='monitor',
            name='creator',
            field=models.ForeignKey(db_constraint=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_query_name='creator_query', to=settings.AUTH_USER_MODEL, verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='monitor',
            name='server',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='monitor.Server', verbose_name='关联服务器信息'),
        ),
    ]
