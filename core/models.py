from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)


class tblUsers(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, db_column='ID')  # Field name made lowercase.
    username = models.CharField(unique=True, max_length=250, default='')
    email = models.EmailField(max_length=250, default='')
    permissionlevel = models.SmallIntegerField(db_column='PermissionLevel', default=0)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=250, default='')  # Field name made lowercase.
    fullname = models.CharField(db_column='FirstName', max_length=250, default='')  # Field name made lowercase.
    designation = models.CharField(db_column='Designation', max_length=250, default='')  # Field name made lowercase.
    createdon = models.DateTimeField(db_column='CreatedOn', default=now)  # Field name made lowercase.
    createdby = models.BigIntegerField(db_column='CreatedBy', default=0)  # Field name made lowercase.
    modifiedon = models.DateTimeField(db_column='ModifiedOn', default=now)  # Field name made lowercase.
    modifiedby = models.BigIntegerField(db_column='ModifiedBy', default=0)  # Field name made lowercase.
    is_staff = models.BooleanField(db_column='IsStaff', default=False) #
    is_active = models.BooleanField(db_column='IsActive', default=True) #

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # Define the field used as the username
    REQUIRED_FIELDS = ['password', 'email']

class tblCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_code = models.CharField(max_length=10, unique=True, default='')
    category_name = models.CharField(max_length=50, default='')
    type = models.CharField(max_length=30, default='stock')
    vat_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)

class tblSalesman(models.Model):
    id = models.BigAutoField(primary_key=True)
    salesman_code = models.CharField(max_length=10, unique=True, default='')
    salesman_name = models.CharField(max_length=100, default='')
    passport_no = models.CharField(max_length=25, default='')
    passport_expiry = models.DateField(default=now)
    visa_no = models.CharField(max_length=25, default='')
    visa_expiry = models.DateField(default=now)
    health_insurance = models.CharField(max_length=25, default='')
    health_insurance_expiry = models.DateField(default=now)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.CharField(max_length=255, default='')
    mobile = models.CharField(max_length=25, default='')
    email = models.EmailField(max_length=200, default='')

    
class tblVendor(models.Model):
    id = models.BigAutoField(primary_key=True)
    vendor_code = models.CharField(max_length=10, unique=True, default='')
    vendor_name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default= '')
    city = models.CharField(max_length=50, default = '', blank=True, null=True)
    state = models.CharField(max_length=50, default = '', blank=True, null=True)
    country = models.CharField(max_length=50, default = '', blank=True, null=True)
    contact_person = models.CharField(max_length=50, default = '', blank=True, null=True)
    mobile = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=20, default = '', blank=True, null=True)
    email = models.EmailField(default='')
    credit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_alert = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_days = models.IntegerField(default=0)

class tblProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_code = models.CharField(max_length=10, unique=True, default='')
    product_name = models.CharField(max_length=255, default='')
    main_unit = models.CharField(max_length=10, default='pcs')
    description = models.TextField(max_length=255, default='', blank=True, null=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    last_purch_price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    stock = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    vendor = models.ForeignKey(tblVendor, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(tblCategory, on_delete=models.PROTECT)

class tblProduct_unit(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(tblProduct, on_delete=models.CASCADE)
    unit = models.CharField(max_length=10, default='')
    multiple = models.CharField(max_length=1, default='*')
    multiple_value = models.DecimalField(max_digits=12, decimal_places=2, default=1)

class tblCustomer(models.Model):
    id = models.BigAutoField(primary_key=True)
    customer_code = models.CharField(max_length=10, unique=True, default='')
    customer_name = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default= '')
    city = models.CharField(max_length=50, default = '', blank=True, null=True)
    state = models.CharField(max_length=50, default = '', blank=True, null=True)
    country = models.CharField(max_length=50, default = '', blank=True, null=True)
    contact_person = models.CharField(max_length=50, default = '', blank=True, null=True)
    mobile = models.CharField(max_length=20, default='')
    phone = models.CharField(max_length=20, default = '', blank=True, null=True)
    email = models.EmailField(default='')
    credit_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    credit_alert = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_days = models.IntegerField(default=0)

class tblSales_Master(models.Model):
    id = models.BigAutoField(primary_key=True)
    return_no = models.CharField(max_length=15, default='', blank=True, null=True)
    invoice_no = models.CharField(max_length=15, default='', blank=True, null=True)
    invoice_date = models.DateField(default=now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roundoff = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_received = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=15, default='cash')
    customer = models.ForeignKey(tblCustomer, on_delete=models.DO_NOTHING)
    salesman = models.ForeignKey(tblSalesman, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(max_length=10, default='', blank=True, null=True)

class tblSales_Details(models.Model):
    id = models.BigAutoField(primary_key=True)
    sales = models.ForeignKey(tblSales_Master, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(tblProduct, on_delete=models.DO_NOTHING, blank=True, null=True)
    unit = models.CharField(max_length=10, default='pcs')
    stock = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, null=True)
    qty = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_perc = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    item_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    
    def get_units(self):
        return tblProduct_unit.objects.filter(product=self.product)

class tblPurchase_Master(models.Model):
    id = models.BigAutoField(primary_key=True)
    return_no = models.CharField(max_length=15, default='', blank=True, null=True)
    invoice_no = models.CharField(max_length=15, default='', blank=True, null=True)
    purchase_no = models.CharField(max_length=15, default='', blank=True, null=True)
    invoice_date = models.DateField(default=now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roundoff = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_payed = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=15, default='cash')
    vendor = models.ForeignKey(tblVendor, on_delete=models.DO_NOTHING)
    salesman = models.ForeignKey(tblSalesman, on_delete=models.DO_NOTHING)
    transaction_type = models.CharField(max_length=10, default='', blank=True, null=True)

class tblPurchase_Details(models.Model):
    id = models.BigAutoField(primary_key=True)
    purchase = models.ForeignKey(tblPurchase_Master, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(tblProduct, on_delete=models.DO_NOTHING, blank=True, null=True)
    unit = models.CharField(max_length=10, default='pcs')
    qty = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_perc = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    item_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    previous_purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    def get_units(self):
        return tblProduct_unit.objects.filter(product=self.product)

class tblSalesOrder_Master(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_no = models.CharField(max_length=15, default='', blank=True, null=True)
    order_date = models.DateField(default=now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roundoff = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    customer = models.ForeignKey(tblCustomer, on_delete=models.DO_NOTHING)
    salesman = models.ForeignKey(tblSalesman, on_delete=models.DO_NOTHING)

class tblSalesOrder_Details(models.Model):
    id = models.BigAutoField(primary_key=True)
    sales_order = models.ForeignKey(tblSalesOrder_Master, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(tblProduct, on_delete=models.DO_NOTHING, blank=True, null=True)
    unit = models.CharField(max_length=10, default='pcs')
    stock = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, null=True)
    qty = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_perc = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    item_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    
    def get_units(self):
        return tblProduct_unit.objects.filter(product=self.product)

class tblPurchaseOrder_Master(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_no = models.CharField(max_length=15, default='', blank=True, null=True)
    order_date = models.DateField(default=now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roundoff = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vendor = models.ForeignKey(tblVendor, on_delete=models.DO_NOTHING)
    salesman = models.ForeignKey(tblSalesman, on_delete=models.DO_NOTHING)
    
class tblPurchaseOrder_Details(models.Model):
    id = models.BigAutoField(primary_key=True)
    purchase_order = models.ForeignKey(tblPurchaseOrder_Master, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(tblProduct, on_delete=models.DO_NOTHING, blank=True, null=True)
    unit = models.CharField(max_length=10, default='pcs')
    qty = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_perc = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    item_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    def get_units(self):
        return tblProduct_unit.objects.filter(product=self.product)
    
class tblQuotation_Master(models.Model):
    id = models.BigAutoField(primary_key=True)
    quotation_no = models.CharField(max_length=15, default='', blank=True, null=True)
    quotation_date = models.DateField(default=now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roundoff = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    customer = models.ForeignKey(tblCustomer, on_delete=models.DO_NOTHING)
    salesman = models.ForeignKey(tblSalesman, on_delete=models.DO_NOTHING)
    
class tblQuotation_Details(models.Model):
    id = models.BigAutoField(primary_key=True)
    quotation = models.ForeignKey(tblQuotation_Master, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(tblProduct, on_delete=models.DO_NOTHING, blank=True, null=True)
    unit = models.CharField(max_length=10, default='pcs')
    qty = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_perc = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    item_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)

    def get_units(self):
        return tblProduct_unit.objects.filter(product=self.product)

class tblDeliveryNote_Master(models.Model):
    id = models.BigAutoField(primary_key=True)
    delivery_note_no = models.CharField(max_length=15, default='', blank=True, null=True)
    delivery_note_date = models.DateField(default=now)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    roundoff = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    customer = models.ForeignKey(tblCustomer, on_delete=models.DO_NOTHING)
    salesman = models.ForeignKey(tblSalesman, on_delete=models.DO_NOTHING)

class tblDeliveryNote_Details(models.Model):
    id = models.BigAutoField(primary_key=True)
    delivery_note = models.ForeignKey(tblDeliveryNote_Master, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(tblProduct, on_delete=models.DO_NOTHING, blank=True, null=True)
    unit = models.CharField(max_length=10, default='pcs')
    stock = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, null=True)
    qty = models.DecimalField(max_digits=12, decimal_places=2,default=0, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_perc = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    vat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    item_discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    
    def get_units(self):
        return tblProduct_unit.objects.filter(product=self.product)

class tblPayment(models.Model):
    id = models.BigAutoField(primary_key=True)
    payment_no = models.IntegerField(default=0, null=True, blank=True)
    payment_date = models.DateField(default=now)
    vendor = models.ForeignKey(tblVendor, on_delete=models.DO_NOTHING, blank=True, null=True)
    payment_to = models.CharField(max_length=150, default="", blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    payment_method = models.CharField(max_length=15, default='cash')
    
class tblReceipt(models.Model):
    id = models.BigAutoField(primary_key=True)
    receipt_no = models.IntegerField(default=0, null=True, blank=True)
    receipt_date = models.DateField(default=now)
    customer = models.ForeignKey(tblCustomer, on_delete=models.DO_NOTHING, blank=True, null=True)
    receipt_from = models.CharField(max_length=150, default="", blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0, blank=True, null=True)
    payment_method = models.CharField(max_length=15, default='cash')
