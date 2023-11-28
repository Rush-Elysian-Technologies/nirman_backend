# Generated by Django 4.2.7 on 2023-11-24 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_servicecategory_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('slug', models.CharField(max_length=300, null=True, unique=True)),
                ('price_per_day', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('price_per_hour', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('price_per_service', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('price_per_sq_feet', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('location', models.CharField(max_length=200)),
                ('contact_number', models.CharField(max_length=20)),
                ('tags', models.TextField(null=True)),
                ('image', models.ImageField(null=True, upload_to='product_imgs')),
                ('demo_url', models.URLField(blank=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_product', to='main.servicecategory')),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='service_imgs/')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_imgs', to='main.service')),
            ],
        ),
    ]
