# Generated by Django 3.2.3 on 2021-06-10 19:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('message', models.TextField(blank=True, default='')),
                ('creation_date', models.DateTimeField(auto_now=True)),
                ('expiry_date', models.DateTimeField(default=None)),
                ('link', models.URLField(blank=True, null=True)),
                ('link_text', models.CharField(default='Get Started', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, default='')),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('description', models.TextField(blank=True, default='This may come as a surprise to you but...')),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='children', to='shop.category')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('price', models.FloatField(default=10.0)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(upload_to='')),
                ('featured', models.BooleanField(default=False)),
                ('top_product', models.BooleanField(default=False)),
                ('discount', models.FloatField(default=0.0)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='products', to='shop.brand')),
                ('categories', models.ManyToManyField(blank=True, to='shop.Category')),
                ('viewers', models.ManyToManyField(blank=True, related_name='viewed_products', to='core.Node')),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.node')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=45)),
                ('cost', models.FloatField(default=10.0)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(null=True, upload_to='')),
                ('quantity', models.IntegerField(default=1)),
                ('ordered', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.node')),
            ],
            options={
                'verbose_name': 'Ordered Item',
                'verbose_name_plural': 'Ordered Items',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.UUIDField(default=uuid.uuid4)),
                ('total_price', models.FloatField(default=0.0)),
                ('calculated', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(auto_now=True)),
                ('processed', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(to='shop.OrderItem')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.node')),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=None, max_length=25)),
                ('discount', models.FloatField(default=0.0)),
                ('applied', models.BooleanField(default=False)),
                ('usage', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now=True)),
                ('expire', models.DateTimeField(default=None)),
                ('orders', models.ManyToManyField(blank=True, to='shop.Order')),
            ],
        ),
    ]