# Generated by Django 4.2.15 on 2024-09-03 21:17


import django.db.models.deletion
from django.db import migrations, models

import auto_validator.core.models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Block",
            fields=[
                ("serial_number", models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ("timestamp", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Hotkey",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "hotkey",
                    models.CharField(
                        max_length=48, unique=True, validators=[auto_validator.core.models.validate_hotkey_length]
                    ),
                ),
                ("is_mother", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Operator",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("discord_id", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Server",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("ip_address", models.GenericIPAddressField()),
                (
                    "ssh_private_key",
                    models.CharField(
                        blank=True, help_text="Path to the SSH private key file", max_length=255, null=True
                    ),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Subnet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                ("operators", models.ManyToManyField(blank=True, related_name="subnets", to="core.operator")),
            ],
        ),
        migrations.CreateModel(
            name="SubnetSlot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "blockchain",
                    models.CharField(choices=[("mainnet", "Mainnet"), ("testnet", "Testnet")], max_length=50),
                ),
                ("netuid", models.IntegerField()),
                (
                    "maximum_registration_price",
                    models.IntegerField(default=0, help_text="Maximum registration price in RAO"),
                ),
                ("restart_threshold", models.IntegerField(default=0)),
                ("reinstall_threshold", models.IntegerField(default=0)),
                (
                    "deregistration_block",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="deregistration_slots",
                        to="core.block",
                    ),
                ),
                (
                    "registration_block",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="registration_slots",
                        to="core.block",
                    ),
                ),
                (
                    "subnet",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="slots",
                        to="core.subnet",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ValidatorInstance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("last_updated", models.PositiveIntegerField(blank=True, null=True)),
                ("status", models.BooleanField(default=False)),
                ("uses_child_hotkey", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "hotkey",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.hotkey"
                    ),
                ),
                (
                    "server",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="validator_instances",
                        to="core.server",
                    ),
                ),
                (
                    "subnet_slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="validator_instances",
                        to="core.subnetslot",
                    ),
                ),
            ],
        ),
    ]