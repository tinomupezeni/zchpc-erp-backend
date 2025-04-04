# Generated by Django 5.2 on 2025-04-03 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0002_rename_nationalid_employees_nationalid'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeductionType',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('mandatory', 'Mandatory'), ('optional', 'Optional')], max_length=20)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Deduction Type',
                'verbose_name_plural': 'Deduction Types',
            },
        ),
        migrations.CreateModel(
            name='InsuranceOption',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('insurance_type', models.CharField(choices=[('funeral', 'Funeral Cover'), ('life', 'Life Insurance')], max_length=20)),
                ('calculation_type', models.CharField(blank=True, choices=[('fixed', 'Fixed Amount'), ('percentage', 'Percentage of Salary')], max_length=30, null=True)),
                ('usd_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('zwl_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('rate', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True)),
                ('min_amount_usd', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('min_amount_zwl', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('max_amount_usd', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('max_amount_zwl', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('cover_details', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Insurance Option',
                'verbose_name_plural': 'Insurance Options',
            },
        ),
        migrations.CreateModel(
            name='MedicalAidProvider',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Medical Aid Provider',
                'verbose_name_plural': 'Medical Aid Providers',
            },
        ),
        migrations.CreateModel(
            name='PensionFund',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('employee_rate', models.DecimalField(decimal_places=4, max_digits=5)),
                ('employer_rate', models.DecimalField(decimal_places=4, max_digits=5)),
                ('currency', models.CharField(choices=[('usd', 'USD Only'), ('zwl', 'ZWL Only'), ('both', 'Both')], max_length=10)),
            ],
            options={
                'verbose_name': 'Pension Fund',
                'verbose_name_plural': 'Pension Funds',
            },
        ),
        migrations.CreateModel(
            name='Union',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('usd_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('zwl_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('frequency', models.CharField(choices=[('monthly', 'Monthly'), ('annual', 'Annual')], max_length=20)),
            ],
            options={
                'verbose_name': 'Union',
                'verbose_name_plural': 'Unions',
            },
        ),
        migrations.RenameField(
            model_name='employees',
            old_name='salary',
            new_name='usd_salary',
        ),
        migrations.AddField(
            model_name='employees',
            name='zig_salary',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='MedicalAidPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('usd_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('zwl_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.medicalaidprovider')),
            ],
            options={
                'verbose_name': 'Medical Aid Plan',
                'verbose_name_plural': 'Medical Aid Plans',
            },
        ),
        migrations.CreateModel(
            name='NSSACap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usd_cap', models.DecimalField(decimal_places=2, max_digits=10)),
                ('zwl_cap', models.DecimalField(decimal_places=2, max_digits=12)),
                ('rate', models.DecimalField(decimal_places=4, max_digits=5)),
                ('contribution_type', models.CharField(choices=[('employee', 'Employee Only'), ('employer', 'Employer Only'), ('employee_and_employer', 'Employee and Employer')], max_length=30)),
                ('deduction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.deductiontype')),
            ],
            options={
                'verbose_name': 'NSSA Cap',
                'verbose_name_plural': 'NSSA Caps',
            },
        ),
        migrations.CreateModel(
            name='PAYETaxCredit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usd_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('zwl_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('deduction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.deductiontype')),
            ],
            options={
                'verbose_name': 'PAYE Tax Credit',
                'verbose_name_plural': 'PAYE Tax Credits',
            },
        ),
        migrations.CreateModel(
            name='PAYEThreshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('ZWL', 'Zimbabwe Dollar')], max_length=3)),
                ('threshold_from', models.DecimalField(decimal_places=2, max_digits=12)),
                ('threshold_to', models.DecimalField(decimal_places=2, max_digits=12)),
                ('rate', models.DecimalField(decimal_places=4, max_digits=5)),
                ('fixed_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('deduction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.deductiontype')),
            ],
            options={
                'verbose_name': 'PAYE Threshold',
                'verbose_name_plural': 'PAYE Thresholds',
            },
        ),
        migrations.CreateModel(
            name='EmployeeDeductables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('ZWL', 'Zimbabwe Dollar')], max_length=3)),
                ('pension_employee_contribution', models.BooleanField(default=True)),
                ('school_fees_benefit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('housing_benefit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('loan_benefit', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('active', models.BooleanField(default=True)),
                ('effective_date', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='erp.employees')),
                ('funeral_cover', models.ForeignKey(blank=True, limit_choices_to={'insurance_type': 'funeral'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='funeral_cover', to='erp.insuranceoption')),
                ('life_insurance', models.ForeignKey(blank=True, limit_choices_to={'insurance_type': 'life'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='life_insurance', to='erp.insuranceoption')),
                ('medical_aid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='erp.medicalaidplan')),
                ('pension_fund', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='erp.pensionfund')),
                ('union', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='erp.union')),
            ],
            options={
                'verbose_name': 'Employee Deductable',
                'verbose_name_plural': 'Employee Deductables',
                'unique_together': {('employee', 'effective_date')},
            },
        ),
    ]
