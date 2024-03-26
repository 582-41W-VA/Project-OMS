# Generated by Django 5.0.3 on 2024-03-16 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Complete", "Complete"),
                    ("Attention Required", "Attention Required"),
                ],
                default="Pending",
                max_length=50,
            ),
        ),
    ]