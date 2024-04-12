# Generated by Django 5.0.3 on 2024-04-05 19:08


# Generated by Django 5.0.2 on 2024-04-05 19:46

# Generated by Django 5.0.3 on 2024-04-08 15:10


import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("image", models.ImageField(upload_to="media/")),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "priority",
                    models.CharField(
                        choices=[("Urgent", "Urgent"), ("Normal", "Normal")],
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Complete", "Complete"),
                            ("Attention Required", "Attention Required"),
                        ],
                        default="Pending",
                        max_length=50,
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "order_assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("comment_text", models.TextField()),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="accounts.order"
                    ),
                ),
            ],
        ),
    ]
