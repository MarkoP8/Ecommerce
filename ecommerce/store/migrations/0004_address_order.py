# Generated by Django 4.0.4 on 2023-05-29 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order'),
        ),
    ]
