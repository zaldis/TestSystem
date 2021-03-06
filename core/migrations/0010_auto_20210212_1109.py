# Generated by Django 3.1.6 on 2021-02-12 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_testresult'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testresult',
            name='user',
        ),
        migrations.AddField(
            model_name='testresult',
            name='user_detail',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='core.userdetail'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userdetail',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
