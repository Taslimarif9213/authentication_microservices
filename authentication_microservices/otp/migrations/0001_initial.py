# Generated by Django 4.2.4 on 2023-08-19 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_type', models.CharField(choices=[('LOGIN', 'LOGIN')], db_column='otp_type', max_length=255)),
                ('otp', models.IntegerField(db_column='otp_code')),
                ('expiry', models.IntegerField(db_column='otp_expiry', default=120)),
                ('mobile_no', models.CharField(db_column='otp_mobile_number', max_length=50)),
                ('is_verified', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'ins_otp',
            },
        ),
    ]