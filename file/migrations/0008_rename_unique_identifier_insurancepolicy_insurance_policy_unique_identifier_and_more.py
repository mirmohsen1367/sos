# Generated by Django 4.2 on 2024-10-04 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0007_alter_planinfo_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='insurancepolicy',
            old_name='unique_identifier',
            new_name='insurance_policy_unique_identifier',
        ),
        migrations.RenameField(
            model_name='insurer',
            old_name='unique_identifier',
            new_name='insurer_unique_identifier',
        ),
        migrations.RenameField(
            model_name='planinfo',
            old_name='unique_identifier',
            new_name='planinfo_unique_identifier',
        ),
        migrations.RenameField(
            model_name='policyholderinfo',
            old_name='unique_identifier',
            new_name='policy_holder_unique_identifier',
        ),
        migrations.AlterUniqueTogether(
            name='insurancepolicy',
            unique_together={('number', 'insurance_policy_unique_identifier', 'insurer')},
        ),
        migrations.AlterUniqueTogether(
            name='insurer',
            unique_together={('name', 'insurer_unique_identifier')},
        ),
        migrations.AlterUniqueTogether(
            name='planinfo',
            unique_together={('name', 'planinfo_unique_identifier', 'insurer')},
        ),
        migrations.AlterUniqueTogether(
            name='policyholderinfo',
            unique_together={('name', 'policy_holder_unique_identifier', 'insurer')},
        ),
    ]
