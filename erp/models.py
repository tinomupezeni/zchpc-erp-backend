from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    employeeid = models.CharField(max_length=10, unique=True, blank=True)
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    department = models.CharField(max_length=50, default='System')
    email = models.EmailField(unique=True)
    salary = models.IntegerField(null=True, blank=True)
    contractFrom = models.DateField(null=True, blank=True)
    contractTo = models.DateField(null=True, blank=True)
    isActive = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.employeeid:
            last_employee = CustomUser.objects.order_by("-id").first()
            if last_employee and last_employee.employeeid:
                last_id = int(last_employee.employeeid.replace("SYS", ""))
                new_id = f"SYS{last_id + 1:04d}"
            else:
                new_id = "SYS0001"
            self.employeeid = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employeeid} - {self.email}"


class Employees(models.Model):
    employeeid = models.CharField(max_length=10, unique=True, blank=True)
    firstname = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    nationalid = models.CharField(max_length=50, unique=True, null=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, blank=True)
    maritalStatus = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50, default='System')
    employee_type = models.CharField(max_length=50, default='Unspecified')
    leave_days = models.IntegerField(default=0)
    contractFrom = models.DateField(null=True, blank=True)
    contractTo = models.DateField(null=True, blank=True)
    usd_salary = models.IntegerField(null=True, blank=True)
    zig_salary = models.IntegerField(null=True, blank=True)
    frequency = models.CharField(max_length=50, default='monthly')
    bankName = models.CharField(max_length=100, blank=True)
    bankAccount = models.CharField(max_length=50, blank=True)
    pensionFund = models.CharField(max_length=100, blank=True)
    nssaNumber = models.CharField(max_length=50, blank=True)
    zimraTaxNumber = models.CharField(max_length=50, blank=True)
    payeNumber = models.CharField(max_length=50, blank=True)
    aidsLevyNumber = models.BooleanField(default=True)
    isActive = models.BooleanField(default=True)
    emegencyContactName = models.CharField(max_length=100, blank=True)
    emegencyContactNumber = models.CharField(max_length=15, blank=True)
    emegencyContactRelationship = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if not self.employeeid:
            last_employee = Employees.objects.order_by("-id").first()
            if last_employee and last_employee.employeeid:
                last_id = int(last_employee.employeeid.replace("EMP", ""))
            else:
                last_id = 0  # Start from EMP0001 if no employees exist
            
            # Keep trying new IDs until we find an available one
            while True:
                last_id += 1
                new_id = f"EMP{last_id:04d}"
                if not Employees.objects.filter(employeeid=new_id).exists():
                    self.employeeid = new_id
                    break

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employeeid} - {self.email}"
    
class ZiGRateToUSD(models.Model):
    date = models.DateField(max_length=50)
    rate = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.rate}"
    
class Payroll(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    baseSalaryUSD = models.CharField(max_length=100)
    baseSalaryZiG = models.CharField(max_length=100)
    exchangeRate = models.ForeignKey(ZiGRateToUSD, on_delete=models.NOT_PROVIDED)
    period = models.DateField(max_length=50)
    
    def __str__(self):
        return f"{self.employee} - {self.period}"

# Base tables for deduction definitions
class DeductionType(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=[('mandatory', 'Mandatory'), ('optional', 'Optional')])
    description = models.TextField()
    
    class Meta:
        verbose_name = "Deduction Type"
        verbose_name_plural = "Deduction Types"


class PAYEThreshold(models.Model):
    deduction_type = models.ForeignKey(DeductionType, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=[('USD', 'US Dollar'), ('ZWL', 'Zimbabwe Dollar')])
    threshold_from = models.DecimalField(max_digits=12, decimal_places=2)
    threshold_to = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=5, decimal_places=4)
    fixed_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = "PAYE Threshold"
        verbose_name_plural = "PAYE Thresholds"

class PAYETaxCredit(models.Model):
    deduction_type = models.ForeignKey(DeductionType, on_delete=models.CASCADE)
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2)
    zwl_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = "PAYE Tax Credit"
        verbose_name_plural = "PAYE Tax Credits"


class NSSACap(models.Model):
    deduction_type = models.ForeignKey(DeductionType, on_delete=models.CASCADE)
    usd_cap = models.DecimalField(max_digits=10, decimal_places=2)
    zwl_cap = models.DecimalField(max_digits=12, decimal_places=2)
    rate = models.DecimalField(max_digits=5, decimal_places=4)
    contribution_type = models.CharField(max_length=30, choices=[('employee', 'Employee Only'),
                                                              ('employer', 'Employer Only'),
                                                              ('employee_and_employer', 'Employee and Employer')])
    
    class Meta:
        verbose_name = "NSSA Cap"
        verbose_name_plural = "NSSA Caps"


class MedicalAidProvider(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = "Medical Aid Provider"
        verbose_name_plural = "Medical Aid Providers"


class MedicalAidPlan(models.Model):
    provider = models.ForeignKey(MedicalAidProvider, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2)
    zwl_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = "Medical Aid Plan"
        verbose_name_plural = "Medical Aid Plans"


class PensionFund(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    employee_rate = models.DecimalField(max_digits=5, decimal_places=4)
    employer_rate = models.DecimalField(max_digits=5, decimal_places=4)
    currency = models.CharField(max_length=10, choices=[('usd', 'USD Only'), ('zwl', 'ZWL Only'), ('both', 'Both')])
    
    class Meta:
        verbose_name = "Pension Fund"
        verbose_name_plural = "Pension Funds"


class InsuranceOption(models.Model):
    INSURANCE_TYPES = [
        ('funeral', 'Funeral Cover'),
        ('life', 'Life Insurance'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPES)
    calculation_type = models.CharField(max_length=30, null=True, blank=True,
                                      choices=[('fixed', 'Fixed Amount'),
                                               ('percentage', 'Percentage of Salary')])
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    zwl_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    min_amount_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_amount_zwl = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_amount_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_amount_zwl = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cover_details = models.CharField(max_length=200, null=True, blank=True)
    
    class Meta:
        verbose_name = "Insurance Option"
        verbose_name_plural = "Insurance Options"


class Union(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2)
    zwl_amount = models.DecimalField(max_digits=12, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('annual', 'Annual')])
    
    class Meta:
        verbose_name = "Union"
        verbose_name_plural = "Unions"


# Employee-specific deductions
class EmployeeDeductables(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('ZWL', 'Zimbabwe Dollar'),
    ]
    
    employee = models.ForeignKey('Employees', on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    
    # Medical Aid
    medical_aid = models.ForeignKey(MedicalAidPlan, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Pension
    pension_fund = models.ForeignKey(PensionFund, on_delete=models.SET_NULL, null=True, blank=True)
    pension_employee_contribution = models.BooleanField(default=True)
    
    # Insurance
    funeral_cover = models.ForeignKey(InsuranceOption, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='funeral_cover', limit_choices_to={'insurance_type': 'funeral'})
    life_insurance = models.ForeignKey(InsuranceOption, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='life_insurance', limit_choices_to={'insurance_type': 'life'})
    
    # Union
    union = models.ForeignKey(Union, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Benefits (for withholding tax)
    school_fees_benefit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    housing_benefit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    loan_benefit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Other fields
    active = models.BooleanField(default=True)
    effective_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Employee Deductable"
        verbose_name_plural = "Employee Deductables"
        unique_together = ('employee', 'effective_date')
    
    def __str__(self):
        return f"Deductions for {self.employee} ({self.currency})"
