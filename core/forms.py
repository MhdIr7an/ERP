from django import forms
from django.db.models import Max, Min

from core.convertions import to_integer

from . models import (tblProduct, tblCustomer, tblVendor, tblCategory, tblSales_Master, tblPurchase_Master, tblSalesman, tblPurchaseOrder_Master, tblDeliveryNote_Master, tblQuotation_Master,
                    tblPayment, tblReceipt, tblSalesOrder_Master)

form_l = { 'class': 'form__size-l floating-input', 'placeholder': ' ' }
form_s = { 'class': 'form__size-s floating-input', 'placeholder': ' ' }
form_l_uppercase = { 'class': 'form__size-l floating-input uppercase-only', 'placeholder': ' ' }
form_s_uppercase = { 'class': 'form__size-s floating-input uppercase-only', 'placeholder': ' ' }
form_s_disabled = { 'class': 'form__size-s floating-input disabled-input', 'placeholder': ' ' }
form_s_select = { 'class': 'form__size-s floating-input' }

uppercase = { 'class': 'uppercase-only' }
autocomplete_off = { 'autocomplete': 'off' }
readOnly = { 'readonly': 'readonly' }

units = [('', ''), ('pcs', 'Pcs'), ('box', 'Box'), ('kg', 'Kg'), ('num', 'Num'), ('ctn', 'Ctn')]
payment_method = [('cash', 'Cash'), ('card', 'Card'), ('bank transfer', 'Bank Transfer'), ('cheque', 'Cheque')]
categories = [('stock', 'Stock'), ('non stock', 'Non Stock'), ('service', 'Service')]

class CategoryForm(forms.ModelForm):
    disabled_class = 'disabled-input'

    class Meta:
        model = tblCategory
        fields = '__all__'
        widgets = {
            'category_code': forms.TextInput(attrs={**form_s_uppercase, **autocomplete_off}),
            'category_name': forms.TextInput(attrs={**form_l_uppercase, **autocomplete_off}),
            'type': forms.Select(attrs=form_s_select, choices=categories),
            'vat_rate': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
        }

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields['vat_rate'].initial = None

class ProductForm(forms.ModelForm):
    disabled_class = 'disabled-input'

    class Meta:
        model = tblProduct
        fields = '__all__'
        widgets = {
            'product_code': forms.TextInput(attrs={**form_s_uppercase, **autocomplete_off, 'id': 'product_code'}),
            'product_name': forms.TextInput(attrs={**form_l_uppercase, **autocomplete_off, 'id': 'product_name'}),
            'main_unit': forms.Select(attrs={**form_s_select, 'id': 'product_main_unit'}, choices=units),
            'description': forms.Textarea(attrs={**form_l, **autocomplete_off, 'id': 'product_description'}),
            'cost_price': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'product_cost_price'}),
            'selling_price': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'product_selling_price'}),
            'stock': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'product_stock'}),
            'vendor': forms.HiddenInput(attrs={**form_l, **autocomplete_off, 'id': 'product_vendor'}),
            'category': forms.HiddenInput(attrs={**form_l, **autocomplete_off, 'id': 'product_category'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Set the initial values for price and stock to None (blank)
        self.fields['cost_price'].initial = None
        self.fields['selling_price'].initial = None
        self.fields['stock'].initial = None
        

class CustomerForm(forms.ModelForm):
    disabled_class = 'disabled-input'

    class Meta:
        model = tblCustomer
        fields = '__all__'
        widgets = {
            'customer_code': forms.TextInput(attrs={**form_s_uppercase, **autocomplete_off}),
            'customer_name': forms.TextInput(attrs={**form_l_uppercase, **autocomplete_off}),
            'address': forms.Textarea(attrs={**form_l, **autocomplete_off}),
            'city': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'state': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'country': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'contact_person': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'mobile': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'phone': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'email': forms.TextInput(attrs={**form_l, **autocomplete_off}),
            'credit_balance': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'credit_limit': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'credit_alert': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'credit_days': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        self.fields['credit_balance'].initial = None
        self.fields['credit_limit'].initial = None
        self.fields['credit_alert'].initial = None
        self.fields['credit_days'].initial = None

class VendorForm(forms.ModelForm):
    disabled_class = 'disabled-input'

    class Meta:
        model = tblVendor
        fields = '__all__'
        widgets = {
            'vendor_code': forms.TextInput(attrs={**form_s_uppercase, **autocomplete_off}),
            'vendor_name': forms.TextInput(attrs={**form_l_uppercase, **autocomplete_off}),
            'address': forms.Textarea(attrs={**form_l, **autocomplete_off}),
            'city': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'state': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'country': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'contact_person': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'mobile': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'phone': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'email': forms.TextInput(attrs={**form_l, **autocomplete_off}),
            'credit_balance': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'credit_limit': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'credit_alert': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'credit_days': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
        }

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)

        self.fields['credit_balance'].initial = None
        self.fields['credit_limit'].initial = None
        self.fields['credit_alert'].initial = None
        self.fields['credit_days'].initial = None

class SalesmanForm(forms.ModelForm):
    disabled_class = 'disabled-input'

    class Meta:
        model = tblSalesman
        fields = '__all__'
        widgets = {
            'salesman_code': forms.TextInput(attrs={**form_s_uppercase, **autocomplete_off}),
            'salesman_name': forms.TextInput(attrs={**form_l_uppercase, **autocomplete_off}),
            'passport_no': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'passport_expiry' : forms.DateInput(attrs={**form_s, 'type': 'date'}),
            'visa_no': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'visa_expiry' : forms.DateInput(attrs={**form_s, 'type': 'date'}),
            'health_insurance': forms.TextInput(attrs={**form_s, **autocomplete_off}),
            'health_insurance_expiry' : forms.DateInput(attrs={**form_s, 'type': 'date'}),
            'salary': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'address': forms.Textarea(attrs={**form_l, **autocomplete_off}),
            'mobile': forms.NumberInput(attrs={**form_s, **autocomplete_off}),
            'email': forms.TextInput(attrs={**form_l, **autocomplete_off}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['mobile'].initial = None
        self.fields['salary'].initial = None
        

class SalesForm(forms.ModelForm):
    disabled_class = 'disabled-input'
    
    class Meta:
        model = tblSales_Master
        fields = '__all__'
        widgets = {
            'invoice_no': forms.TextInput(attrs={**form_s, 'id': 'master_invoice_no', **autocomplete_off}),
            'invoice_date': forms.DateInput(attrs={**form_s, 'type': 'date', 'id': 'master_invoice_date'}),
            'return_no': forms.TextInput(attrs={**form_s_disabled, 'id': 'master_return_no', **autocomplete_off, **readOnly}),
            'total': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_total'}),
            'vat': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_vat'}),
            'discount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_discount'}),
            'roundoff': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'master_roundoff'}),
            'net_amount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_net_amount'}),
            'amount_received': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'master_amount_received'}),
            'balance': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_balance' }),
            'payment_method': forms.Select(attrs={**form_s_select, 'id': 'master_payment_method'}, choices=payment_method),
            'customer': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_customer_id'}),
            'salesman': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_salesman_id'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        highest_invoice_no = tblSales_Master.objects.aggregate(max_invoice_no=Max('invoice_no'))['max_invoice_no']
        self.fields['invoice_no'].initial = to_integer(highest_invoice_no) + 1 if highest_invoice_no is not None else 1

        highest_return_no = tblSales_Master.objects.aggregate(max_return_no=Max('return_no'))['max_return_no']
        self.fields['return_no'].initial = to_integer(highest_return_no) + 1 if highest_return_no is not None else 1

        self.fields['total'].initial = None
        self.fields['vat'].initial = None
        self.fields['discount'].initial = None
        self.fields['net_amount'].initial = None
        self.fields['amount_received'].initial = None
        self.fields['balance'].initial = None
        self.fields['customer'].initial = None
        self.fields['salesman'].initial = None
        self.fields['roundoff'].initial = None


class PurchaseForm(forms.ModelForm):
    disabled_class = 'disabled-input'
    
    class Meta:
        model = tblPurchase_Master
        fields = '__all__'
        widgets = {
            'invoice_no': forms.TextInput(attrs={**form_s, 'id': 'master_invoice_no', **autocomplete_off}),
            'purchase_no': forms.TextInput(attrs={**form_s_uppercase, 'id': 'master_purchase_no', **autocomplete_off}),
            'return_no': forms.TextInput(attrs={**form_s_disabled, 'id': 'master_return_no', **autocomplete_off, **readOnly}),
            'invoice_date': forms.DateInput(attrs={**form_s, 'type': 'date', 'id': 'master_invoice_date'}),
            'total': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_total'}),
            'vat': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_vat'}),
            'discount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_discount'}),
            'roundoff': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'master_roundoff'}),
            'net_amount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_net_amount'}),
            'amount_payed': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'master_amount_payed'}),
            'balance': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_balance' }),
            'payment_method': forms.Select(attrs={**form_s_select, 'id': 'master_payment_method'}, choices=payment_method),
            'vendor': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_vendor_id'}),
            'salesman': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_salesman_id'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        highest_invoice_no = tblPurchase_Master.objects.aggregate(max_invoice_no=Max('invoice_no'))['max_invoice_no']
        self.fields['invoice_no'].initial = to_integer(highest_invoice_no) + 1 if highest_invoice_no is not None else 1
        
        highest_return_no = tblPurchase_Master.objects.aggregate(max_return_no=Max('return_no'))['max_return_no']
        self.fields['return_no'].initial = to_integer(highest_return_no) + 1 if highest_return_no is not None else 1

        self.fields['total'].initial = None
        self.fields['vat'].initial = None
        self.fields['discount'].initial = None
        self.fields['net_amount'].initial = None
        self.fields['amount_payed'].initial = None
        self.fields['balance'].initial = None
        self.fields['vendor'].initial = None
        self.fields['salesman'].initial = None
        self.fields['roundoff'].initial = None


class SalesOrderForm(forms.ModelForm):
    disabled_class = 'disabled-input'
    
    class Meta:
        model = tblSalesOrder_Master
        fields = '__all__'
        widgets = {
            'order_no': forms.TextInput(attrs={**form_s_disabled, 'id': 'master_order_no', **autocomplete_off}),
            'order_date': forms.DateInput(attrs={**form_s, 'type': 'date', 'id': 'master_order_date'}),
            'total': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_total'}),
            'vat': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_vat'}),
            'discount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_discount'}),
            'roundoff': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'master_roundoff'}),
            'net_amount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_net_amount'}),
            'customer': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_customer_id'}),
            'salesman': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_salesman_id'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        highest_order_no = tblSalesOrder_Master.objects.aggregate(max_order_no=Max('order_no'))['max_order_no']
        self.fields['order_no'].initial = to_integer(highest_order_no) + 1 if highest_order_no is not None else 1

        self.fields['total'].initial = None
        self.fields['vat'].initial = None
        self.fields['discount'].initial = None
        self.fields['net_amount'].initial = None
        self.fields['customer'].initial = None
        self.fields['salesman'].initial = None
        self.fields['roundoff'].initial = None


class PurchaseOrderForm(forms.ModelForm):
    disabled_class = 'disabled-input'
    
    class Meta:
        model = tblPurchaseOrder_Master
        fields = '__all__'
        widgets = {
            'order_no': forms.TextInput(attrs={**form_s_disabled, 'id': 'master_order_no', **autocomplete_off}),
            'order_date': forms.DateInput(attrs={**form_s, 'type': 'date', 'id': 'master_order_date'}),
            'total': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_total'}),
            'vat': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_vat'}),
            'discount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_discount'}),
            'roundoff': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'master_roundoff'}),
            'net_amount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_net_amount'}),
            'vendor': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_vendor_id'}),
            'salesman': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_salesman_id'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        highest_order_no = tblPurchaseOrder_Master.objects.aggregate(max_order_no=Max('order_no'))['max_order_no']
        self.fields['order_no'].initial = to_integer(highest_order_no) + 1 if highest_order_no is not None else 1

        self.fields['total'].initial = None
        self.fields['vat'].initial = None
        self.fields['discount'].initial = None
        self.fields['net_amount'].initial = None
        self.fields['vendor'].initial = None
        self.fields['salesman'].initial = None
        self.fields['roundoff'].initial = None



class QuotationForm(forms.ModelForm):
    disabled_class = 'disabled-input'
    
    class Meta:
        model = tblQuotation_Master
        fields = '__all__'
        widgets = {
            'quotation_no': forms.TextInput(attrs={**form_s_disabled, 'id': 'master_quotation_no', **autocomplete_off}),
            'quotation_date': forms.DateInput(attrs={**form_s, 'type': 'date', 'id': 'master_quotation_date'}),
            'total': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_total'}),
            'vat': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_vat'}),
            'discount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_discount'}),
            'roundoff': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'master_roundoff'}),
            'net_amount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_net_amount'}),
            'customer': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_customer_id'}),
            'salesman': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_salesman_id'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        highest_quotation_no = tblQuotation_Master.objects.aggregate(max_quotation_no=Max('quotation_no'))['max_quotation_no']
        self.fields['quotation_no'].initial = to_integer(highest_quotation_no) + 1 if highest_quotation_no is not None else 1

        self.fields['total'].initial = None
        self.fields['vat'].initial = None
        self.fields['discount'].initial = None
        self.fields['net_amount'].initial = None
        self.fields['customer'].initial = None
        self.fields['salesman'].initial = None
        self.fields['roundoff'].initial = None


class DeliveryNoteForm(forms.ModelForm):
    disabled_class = 'disabled-input'
    
    class Meta:
        model = tblDeliveryNote_Master
        fields = '__all__'
        widgets = {
            'delivery_note_no': forms.TextInput(attrs={**form_s_disabled, 'id': 'master_delivery_note_no', **autocomplete_off}),
            'delivery_note_date': forms.DateInput(attrs={**form_s, 'type': 'date', 'id': 'master_delivery_note_date'}),
            'total': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_total'}),
            'vat': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_vat'}),
            'discount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_discount'}),
            'roundoff': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'master_roundoff'}),
            'net_amount': forms.NumberInput(attrs={**form_s_disabled, **autocomplete_off, **readOnly, 'id': 'master_net_amount'}),
            'customer': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_customer_id'}),
            'salesman': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'master_salesman_id'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        highest_delivery_note_no = tblDeliveryNote_Master.objects.aggregate(max_delivery_note_no=Max('delivery_note_no'))['max_delivery_note_no']
        self.fields['delivery_note_no'].initial = to_integer(highest_delivery_note_no) + 1 if highest_delivery_note_no is not None else 1

        self.fields['total'].initial = None
        self.fields['vat'].initial = None
        self.fields['discount'].initial = None
        self.fields['net_amount'].initial = None
        self.fields['customer'].initial = None
        self.fields['salesman'].initial = None
        self.fields['roundoff'].initial = None


class PaymentForm(forms.ModelForm):
    disabled_class = 'disabled-input'
    
    class Meta:
        model = tblPayment
        fields = '__all__'
        widgets = {
            'payment_no': forms.TextInput(attrs={**form_s_disabled, 'id': 'payment_no', **autocomplete_off}),
            'payment_date': forms.DateInput(attrs={**form_s, 'type': 'date', 'id': 'payment_date'}),
            'vendor': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'vendor_id'}),
            'payment_to': forms.TextInput(attrs={**form_l, **autocomplete_off, 'id': 'payment_to'}),
            'amount': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'amount'}),
            'discount': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'discount'}),
            'payment_method': forms.Select(attrs={**form_s_select, 'id': 'payment_method'}, choices=payment_method),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        highest_payment_no = tblPayment.objects.aggregate(max_payment_no=Max('payment_no'))['max_payment_no']
        self.fields['payment_no'].initial = to_integer(highest_payment_no) + 1 if highest_payment_no is not None else 1

        
        self.fields['amount'].initial = None
        self.fields['discount'].initial = None


class ReceiptForm(forms.ModelForm):
    disabled_class = 'disabled-input'
    
    class Meta:
        model = tblReceipt
        fields = '__all__'
        widgets = {
            'receipt_no': forms.TextInput(attrs={**form_s_disabled, 'id': 'receipt_no', **autocomplete_off}),
            'receipt_date': forms.DateInput(attrs={**form_s, 'type': 'date', 'id': 'receipt_date'}),
            'receipt_from': forms.TextInput(attrs={**form_l, **autocomplete_off, 'id': 'receipt_from'}),
            'customer': forms.HiddenInput(attrs={**form_s, **autocomplete_off, 'id': 'customer_id'}),
            'amount': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'amount'}),
            'discount': forms.NumberInput(attrs={**form_s, **autocomplete_off, 'id': 'discount'}),
            'payment_method': forms.Select(attrs={**form_s_select, 'id': 'payment_method'}, choices=payment_method),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        highest_receipt_no = tblReceipt.objects.aggregate(max_receipt_no=Max('receipt_no'))['max_receipt_no']
        self.fields['receipt_no'].initial = to_integer(highest_receipt_no) + 1 if highest_receipt_no is not None else 1

        self.fields['amount'].initial = None
        self.fields['discount'].initial = None