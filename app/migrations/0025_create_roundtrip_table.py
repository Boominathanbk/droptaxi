from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_remove_roundtrip_drive'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoundTrip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup', models.CharField(max_length=255, null=True, blank=True)),
                ('drop', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.EmailField(max_length=100, null=True, blank=True)),
                ('date', models.CharField(max_length=15, null=True, blank=True)),
                ('time', models.FloatField(null=True, blank=True)),
                ('number_of_days', models.IntegerField()),
                ('distance', models.FloatField(null=True, blank=True)),
                ('fare', models.CharField(max_length=100, null=True, blank=True)),
                ('total', models.CharField(max_length=100, null=True, blank=True)),
                ('drivercharge', models.CharField(max_length=100, null=True, blank=True)),
                ('carType', models.CharField(max_length=100, null=True, blank=True)),
                ('status', models.CharField(max_length=20, default='Pending')),
                ('is_approved', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('round', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)),
            ],
        ),
    ]
