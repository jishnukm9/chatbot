# Generated by Django 5.1.2 on 2024-11-01 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='context',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddIndex(
            model_name='conversation',
            index=models.Index(fields=['session_id'], name='chatapp_con_session_d8578c_idx'),
        ),
    ]
