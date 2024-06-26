# Generated by Django 5.0.3 on 2024-04-02 22:01

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_title', models.CharField(default='Item', max_length=512)),
                ('description', models.TextField(default='Item Description', max_length=1500)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('highestBid', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('startingBid', models.DecimalField(decimal_places=2, max_digits=12)),
                ('category', models.CharField(max_length=100)),
                ('auctionOpen', models.BooleanField(default=True)),
                ('item_image', models.CharField(blank=True, max_length=2048)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listed_by', to=settings.AUTH_USER_MODEL, to_field='username')),
                ('winner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='winner', to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_title', models.TextField(default='Customer Review', max_length=100)),
                ('comment', models.TextField(max_length=5000)),
                ('commentDate', models.DateTimeField(auto_now_add=True)),
                ('commentBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('bidDate', models.DateTimeField(auto_now_add=True)),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
            ],
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'unique_together': {('listing', 'user')},
            },
        ),
    ]
