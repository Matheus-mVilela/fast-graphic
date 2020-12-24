# Generated by Django 3.1.4 on 2020-12-24 14:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_change', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(max_length=20)),
                (
                    'role',
                    models.CharField(
                        choices=[
                            ('seller', 'Vendedor(a)'),
                            ('administrator', 'Administrador(a)'),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    'user',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={'abstract': False,},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_change', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=35)),
                ('price', models.FloatField()),
                (
                    'description',
                    models.CharField(blank=True, max_length=50, null=True),
                ),
            ],
            options={'abstract': False,},
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_change', models.DateTimeField(auto_now=True)),
                ('discount', models.FloatField()),
                (
                    'employee',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='application.employee',
                    ),
                ),
            ],
            options={'abstract': False,},
        ),
        migrations.CreateModel(
            name='SaleProduct',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_change', models.DateTimeField(auto_now=True)),
                ('quantity', models.FloatField()),
                ('unit_price', models.FloatField()),
                (
                    'product',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='application.product',
                    ),
                ),
                (
                    'sale',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='application.sale',
                    ),
                ),
            ],
            options={'abstract': False,},
        ),
    ]
