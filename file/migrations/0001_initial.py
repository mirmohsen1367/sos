# Generated by Django 4.2 on 2024-09-30 03:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IndividualInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(regex='^09\\d{9}$')])),
                ('national_code', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(regex='^\\d{10}$')])),
                ('birthdate', models.DateField()),
                ('father_name', models.CharField(blank=True, max_length=30, null=True)),
                ('issue_place', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'individual_information',
            },
        ),
        migrations.CreateModel(
            name='InsurancePolicy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('verify_date', models.DateField(blank=True, null=True)),
                ('unique_identifier', models.CharField(max_length=20, unique=True)),
                ('individual_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_policy', to='file.individualinformation')),
            ],
            options={
                'db_table': 'insurance_policy',
            },
        ),
        migrations.CreateModel(
            name='PolicyHolderInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('policy_holder_name', models.CharField(max_length=30)),
                ('unique_identifier', models.CharField(max_length=20)),
                ('individual_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='policy_holder', to='file.individualinformation')),
            ],
            options={
                'db_table': 'policy_holder_info',
                'unique_together': {('policy_holder_name', 'unique_identifier')},
            },
        ),
        migrations.CreateModel(
            name='PlanInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('insurance_policy_number', models.CharField(max_length=20)),
                ('plan_name', models.CharField(choices=[('silver_plan', 'طرح نقره ایی'), ('golden_plan', 'طرح طلایی')], max_length=20)),
                ('unique_identifier', models.CharField(max_length=20)),
                ('individual_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='plan_info', to='file.individualinformation')),
            ],
            options={
                'db_table': 'plan_info',
                'unique_together': {('plan_name', 'unique_identifier')},
            },
        ),
        migrations.CreateModel(
            name='InsurerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('insurer_name', models.CharField(choices=[('MEL', 'ملت'), ('ASI', 'آسیا'), ('HEK', 'حکمت')], max_length=3)),
                ('unique_identifier', models.CharField(max_length=20)),
                ('individual_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='insurer_info', to='file.individualinformation')),
            ],
            options={
                'db_table': 'insurer_info',
                'unique_together': {('insurer_name', 'unique_identifier')},
            },
        ),
    ]
