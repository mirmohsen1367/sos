# Generated by Django 4.2 on 2024-10-13 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0014_alter_insurancepolicy_insurance_policy_unique_identifier'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='insurancepolicy',
            unique_together={('insurance_policy_number', 'insurance_policy_unique_identifier', 'insurer', 'policy_holder_info')},
        ),
    ]
