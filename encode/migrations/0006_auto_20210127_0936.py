# Generated by Django 2.2.17 on 2021-01-27 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('encode', '0005_auto_20210127_0910'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediabase',
            name='reference_content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='mediabase',
            name='reference_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
