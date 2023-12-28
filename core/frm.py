from django.forms.models import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from core.convertions import to_decimal


from .models import (tblProduct, tblCustomer, tblProduct_unit, tblSales_Details, tblVendor, tblCategory, tblSales_Master, tblPurchase_Master, tblPurchase_Details, tblSalesman, tblSalesOrder_Master,
                    tblSalesOrder_Details, tblDeliveryNote_Details, tblDeliveryNote_Master, tblPayment, tblPurchaseOrder_Details, tblPurchaseOrder_Master, tblQuotation_Details, tblQuotation_Master,
                    tblReceipt)
from .forms import (ProductForm, CustomerForm, VendorForm, CategoryForm, SalesForm, PurchaseForm, SalesOrderForm, PurchaseOrderForm, SalesmanForm,
                    QuotationForm, DeliveryNoteForm, ReceiptForm, PaymentForm)


class idExists:
    """
    Checks if next or previous id exists using current id
    """
    def __init__(self, tbl, frm_id, module_name):
        self.tbl = tbl
        self.frm_id = frm_id
        self.module_name = module_name
    def nextId(self):
        filter_condition = {'id__gt': self.frm_id}
        if self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
            filter_condition['transaction_type'] = 'return'
        elif self.module_name == 'sales' or self.module_name == 'purchase': 
            filter_condition['transaction_type'] = ''        
        nxt = self.tbl.objects.filter(**filter_condition).order_by('id').first()
        return bool(nxt)

    def prevId(self):
        filter_condition = {'id__lt': self.frm_id}
        if self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
            filter_condition['transaction_type'] = 'return'
        elif self.module_name == 'sales' or self.module_name == 'purchase': 
            filter_condition['transaction_type'] = ''   
        prev = self.tbl.objects.filter(**filter_condition).order_by('-id').first()
        return bool(prev)

    
    def getNextID(self):
        filter_condition = {'id__gt': self.frm_id}
        if self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
            filter_condition['transaction_type'] = 'return'
        elif self.module_name == 'sales' or self.module_name == 'purchase': 
            filter_condition['transaction_type'] = ''
        nxt = self.tbl.objects.filter(**filter_condition).order_by('id').first()
        return model_to_dict(nxt)['id']

    def getPrevID(self):
        filter_condition = {'id__lt': self.frm_id}
        if self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
            filter_condition['transaction_type'] = 'return'
        elif self.module_name == 'sales' or self.module_name == 'purchase': 
            filter_condition['transaction_type'] = ''

        prev = self.tbl.objects.filter(**filter_condition).order_by('-id').first()
        return model_to_dict(prev)['id']

    def findId(self):
        return self.nextId() or self.prevId()

class model_mapping:
    """
    request: http request object
    module_name: name of the module eg: 'customer', 'product', 'sales'.
    frm_id: id of the Model


    To perform form actions like add, edit, delete, move.
    """
    def __init__(self, request, module_name: str, frm_id=None):
        models = {
            "product": (tblProduct, ProductForm, 'product/view.html', 'product/add.html', 'product/edit.html', 'product/list.html'),
            "customer": (tblCustomer, CustomerForm, 'customer/view.html', 'customer/add.html', 'customer/add.html', 'customer/list.html'),
            "vendor": (tblVendor, VendorForm, 'vendor/view.html', 'vendor/add.html', 'vendor/add.html', 'vendor/list.html'),
            "category": (tblCategory, CategoryForm, 'category/view.html', 'category/add.html', 'category/add.html', 'category/list.html'),
            "salesman": (tblSalesman, SalesmanForm, 'salesman/view.html', 'salesman/add.html', 'salesman/add.html', 'salesman/list.html'),
            "sales": (tblSales_Master, SalesForm, 'sales/view.html', 'sales/add.html', 'sales/edit.html', 'sales/list.html'),
            "purchase": (tblPurchase_Master, PurchaseForm, 'purchase/view.html', 'purchase/add.html', 'purchase/edit.html', 'purchase/list.html'),
            "salesReturn": (tblSales_Master, SalesForm, 'salesReturn/view.html', 'salesReturn/add.html', 'salesReturn/edit.html', 'salesReturn/list.html'),
            "purchaseReturn": (tblPurchase_Master, PurchaseForm, 'purchaseReturn/view.html', 'purchaseReturn/add.html', 'purchaseReturn/edit.html', 'purchaseReturn/list.html'),
            "purchaseOrder": (tblPurchaseOrder_Master, PurchaseOrderForm, 'purchaseOrder/view.html', 'purchaseOrder/add.html', 'purchaseOrder/edit.html', 'purchaseOrder/list.html'),
            "salesOrder": (tblSalesOrder_Master, SalesOrderForm, 'salesOrder/view.html', 'salesOrder/add.html', 'salesOrder/edit.html', 'salesOrder/list.html'),
            "deliveryNote": (tblDeliveryNote_Master, DeliveryNoteForm, 'deliveryNote/view.html', 'deliveryNote/add.html', 'deliveryNote/edit.html', 'deliveryNote/list.html'),
            "quotation": (tblQuotation_Master, QuotationForm, 'quotation/view.html', 'quotation/add.html', 'quotation/edit.html', 'quotation/list.html'),
            "payment": (tblPayment, PaymentForm, 'payment/view.html', 'payment/add.html', 'payment/add.html', 'payment/list.html'),
            "receipt": (tblReceipt, ReceiptForm, 'receipt/view.html', 'receipt/add.html', 'receipt/add.html', 'receipt/list.html'),
        }
        self.module_name = module_name
        self.frm_id = frm_id
        self.request = request
        if module_name in models:
            self.model, self.form_class, self.view_template, self.add_template, self.edit_template, self.list_template = models[module_name]
            # print(get_object_or_404(self.model, id=self.frm_id).id)
        else:
            # Handle invalid module name here
            return redirect('home')
        
    def frm_view(self):
        """
        View a form.
        """
        if self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
            tbl = get_object_or_404(self.model, id=self.frm_id, transaction_type = 'return') if self.frm_id else self.model.objects.filter(transaction_type='return').last()
        elif self.module_name == 'sales' or self.module_name == 'purchase':
            tbl = get_object_or_404(self.model, id=self.frm_id, transaction_type = '') if self.frm_id else self.model.objects.filter(transaction_type='').last()
        else:
            tbl = get_object_or_404(self.model, id=self.frm_id) if self.frm_id else self.model.objects.last()
        if tbl is None:
            return redirect(f'{self.module_name}_add')

        find_checker = idExists(self.model, tbl.id, self.module_name)

        nxt = find_checker.nextId()
        prev = find_checker.prevId()
        find = find_checker.findId()

        values = {
            'next': nxt,
            'prev': prev,
            'find': find,
            'id': tbl.id,
        }
        
        form = self.form_class(instance=tbl)
        context = {'form': form, 'values': values}

        if self.module_name == 'product':
            units = tblProduct_unit.objects.filter(product = tbl)
            context.update({'units': units, 'vendor': tbl.vendor, 'category': tbl.category})
        elif self.module_name == 'sales' or self.module_name == 'salesReturn':
            details = tblSales_Details.objects.filter(sales = tbl)
            context.update({'details': details, 'customer': tbl.customer, 'salesman': tbl.salesman})
        elif self.module_name == 'purchase' or self.module_name == 'purchaseReturn':
            details = tblPurchase_Details.objects.filter(purchase = tbl)
            context.update({'details': details, 'vendor': tbl.vendor, 'salesman': tbl.salesman})
        elif self.module_name == 'salesOrder':
            details = tblSalesOrder_Details.objects.filter(sales_order = tbl)
            context.update({'details': details, 'customer': tbl.customer, 'salesman': tbl.salesman})
        elif self.module_name == 'purchaseOrder':
            details = tblPurchaseOrder_Details.objects.filter(purchase_order = tbl)
            context.update({'details': details, 'vendor': tbl.vendor, 'salesman': tbl.salesman})
        elif self.module_name == 'quotation':
            details = tblQuotation_Details.objects.filter(quotation = tbl)
            context.update({'details': details, 'customer': tbl.customer, 'salesman': tbl.salesman})
        elif self.module_name == 'deliveryNote':
            details = tblDeliveryNote_Details.objects.filter(delivery_note = tbl)
            context.update({'details': details, 'customer': tbl.customer, 'salesman': tbl.salesman})
        elif self.module_name == 'payment':
            context.update({'vendor': tbl.vendor})
        elif self.module_name == 'receipt':
            context.update({'customer': tbl.customer})
        return render(self.request, self.view_template, context)

    @transaction.atomic
    def frm_add(self):
        """
        Add a form.
        """

        if self.request.method == 'POST':
            if (self.module_name == 'product' or self.module_name == 'sales' or self.module_name == 'purchase' or self.module_name == 'salesReturn' or 
                self.module_name == 'purchaseReturn' or self.module_name == 'purchaseOrder' or self.module_name == 'salesOrder' or 
                self.module_name == 'quotation' or self.module_name == 'deliveryNote' or self.module_name == 'payment' or self.module_name == 'receipt'):
                return redirect(self.module_name)
            else:
                form = self.form_class(self.request.POST)  # Create a form instance with POST data
                if form.is_valid():  # Check if the form data is valid
                    form.save()  # Save the form data to the database
                    return redirect(self.module_name)
                else:
                    for field_name, errors in form.errors.items():
                        # 'field_name' is the name of the form field
                        # 'errors' is a list of error messages for that field
                        for error in errors:
                            messages.error(self.request, f"Field '{field_name}': {error}")

        else:
            if self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
                form = self.form_class(initial= {'invoice_no': None})
            else:
                form = self.form_class()  # Create a blank form

        return render(self.request, self.add_template, {'form': form})

    @transaction.atomic
    def frm_edit(self):
        """
        Edit a form.
        """

        tbl = get_object_or_404(self.model, id=self.frm_id)
        if self.request.method == 'POST':
            if self.module_name == ('product' or self.module_name == 'sales'  or self.module_name == 'purchase' or self.module_name == 'salesReturn' or 
                                    self.module_name == 'purchaseReturn' or self.module_name == 'salesOrder' or self.module_name == 'purchaseOrder' or 
                                    self.module_name == 'quotation' or self.module_name == 'deliveryNote' or self.module_name == 'payment' or self.module_name == 'receipt'):
                return redirect(f'{self.module_name}_with_id', self.frm_id)
            else:
                form = self.form_class(self.request.POST, instance=tbl)  # Create a form instance with POST data
                if form.is_valid():  # Check if the form data is valid
                    form.save()  # Save the form data to the database
                    return redirect(f'{self.module_name}_with_id', self.frm_id)
                else:
                    for field_name, errors in form.errors.items():
                        # 'field_name' is the name of the form field
                        # 'errors' is a list of error messages for that field
                        for error in errors:
                            messages.error(self.request, f"Field '{field_name}': {error}")
        else:
            form = self.form_class(instance=tbl)  # Create a blank form

        context = {'form': form, 'id': tbl.id}
        if self.module_name == 'product':
            units = tblProduct_unit.objects.filter(product = tbl)
            context.update({'units': units, 'vendor': tbl.vendor, 'category': tbl.category})
        elif self.module_name == 'sales' or self.module_name == 'salesReturn':
            details = tblSales_Details.objects.filter(sales = tbl)
            context.update({'details': details, 'customer': tbl.customer, 'salesman': tbl.salesman})
        elif self.module_name == 'purchase' or self.module_name == 'purchaseReturn':
            details = tblPurchase_Details.objects.filter(purchase = tbl)
            context.update({'details': details, 'vendor': tbl.vendor, 'salesman': tbl.salesman})
        elif self.module_name == 'salesOrder':
            details = tblSalesOrder_Details.objects.filter(sales_order = tbl)
            context.update({'details': details, 'customer': tbl.customer, 'salesman': tbl.salesman})
        elif self.module_name == 'purchaseOrder':
            details = tblPurchaseOrder_Details.objects.filter(purchase_order = tbl)
            context.update({'details': details, 'vendor': tbl.vendor, 'salesman': tbl.salesman})
        elif self.module_name == 'quotation':
            details = tblQuotation_Details.objects.filter(quotation = tbl)
            context.update({'details': details, 'customer': tbl.customer, 'salesman': tbl.salesman})
        elif self.module_name == 'deliveryNote':
            details = tblDeliveryNote_Details.objects.filter(delivery_note = tbl)
            context.update({'details': details, 'customer': tbl.customer, 'salesman': tbl.salesman})
        elif self.module_name == 'payment':
            context.update({'vendor': tbl.vendor})
        elif self.module_name == 'receipt':
            context.update({'customer': tbl.customer})
        return render(self.request, self.edit_template, context)


    @transaction.atomic
    def frm_delete(self):
        """
        Delete a form.
        """
        
        tbl = self.model.objects.get(id = self.frm_id)
        if self.module_name == 'sales':
            customer = tblCustomer.objects.get(id = tbl.customer.id)
            customer.credit_balance = to_decimal(customer.credit_balance) - to_decimal(tbl.balance)
            customer.save()
            tbl_detail = tblSales_Details.objects.filter(sales = tbl.id)
            for details in tbl_detail:
                product = tblProduct.objects.get(id = details.product.id)
                
                if product.main_unit == details.unit:
                    multiple = 1
                else:
                    prod_unit = tblProduct_unit.objects.get(product = product, unit = details.unit)
                    if prod_unit.multiple == '*':
                        multiple = 1/to_decimal(prod_unit.multiple_value)
                    else:
                        multiple = to_decimal(prod_unit.multiple_value)

                product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))+(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) + (to_decimal(details.qty)*multiple))
                product.stock = to_decimal(product.stock) + (to_decimal(details.qty) * multiple)
                product.save()

        elif self.module_name == 'purchase':
            vendor = tblVendor.objects.get(id = tbl.vendor.id)
            vendor.credit_balance = to_decimal(vendor.credit_balance) - to_decimal(tbl.balance)
            vendor.save()
            tbl_detail = tblPurchase_Details.objects.filter(purchase = tbl.id)
            for details in tbl_detail:
                product = tblProduct.objects.get(id = details.product.id)
                
                if product.main_unit == details.unit:
                    multiple = 1
                else:
                    prod_unit = tblProduct_unit.objects.get(product = product, unit = details.unit)
                    if prod_unit.multiple == '*':
                        multiple = 1/to_decimal(prod_unit.multiple_value)
                    else:
                        multiple = to_decimal(prod_unit.multiple_value)

                product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))-(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) - (to_decimal(details.qty)*multiple))
                product.stock = to_decimal(product.stock) - (to_decimal(details.qty) * multiple)
                product.last_purch_price = to_decimal(details.previous_purchase_price)
                product.save()

        elif self.module_name == 'salesReturn':
            customer = tblCustomer.objects.get(id = tbl.customer.id)
            customer.credit_balance = to_decimal(customer.credit_balance) + to_decimal(tbl.balance)
            customer.save()
            tbl_detail = tblSales_Details.objects.filter(sales = tbl.id)
            for details in tbl_detail:
                product = tblProduct.objects.get(id = details.product.id)

                if product.main_unit == details.unit:
                    multiple = 1
                else:
                    prod_unit = tblProduct_unit.objects.get(product = product, unit = details.unit)
                    if prod_unit.multiple == '*':
                        multiple = 1/to_decimal(prod_unit.multiple_value)
                    else:
                        multiple = to_decimal(prod_unit.multiple_value)

                product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))-(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) - (to_decimal(details.qty)*multiple))
                product.stock = to_decimal(product.stock) - (to_decimal(details.qty) * multiple)
                product.save()

        elif self.module_name == 'purchaseReturn':
            vendor = tblVendor.objects.get(id = tbl.vendor.id)
            vendor.credit_balance = to_decimal(vendor.credit_balance) + to_decimal(tbl.balance)
            vendor.save()
            tbl_detail = tblPurchase_Details.objects.filter(purchase = tbl.id)
            for details in tbl_detail:
                product = tblProduct.objects.get(id = details.product.id)

                if product.main_unit == details.unit:
                    multiple = 1
                else:
                    prod_unit = tblProduct_unit.objects.get(product = product, unit = details.unit)
                    if prod_unit.multiple == '*':
                        multiple = 1/to_decimal(prod_unit.multiple_value)
                    else:
                        multiple = to_decimal(prod_unit.multiple_value)

                product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))+(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) + (to_decimal(details.qty)*multiple))
                product.stock = to_decimal(product.stock) + (to_decimal(details.qty) * multiple)
                product.save()
        
        elif self.module_name == 'payment':
            if tbl.vendor is not None:
                vendor = tblVendor.objects.get(id = tbl.vendor.id)
                vendor.credit_balance = to_decimal(vendor.credit_balance) + to_decimal(tbl.discount) + to_decimal(tbl.amount)
                vendor.save()
        
        elif self.module_name == 'receipt':
            if tbl.customer is not None:
                customer = tblCustomer.objects.get(id = tbl.customer.id)
                customer.credit_balance = to_decimal(customer.credit_balance) + to_decimal(tbl.discount) + to_decimal(tbl.amount)
                customer.save()
        tbl.delete()
        id_exists = idExists(self.model, self.frm_id, self.module_name)
        if not id_exists.findId():
            return redirect(f'{self.module_name}_add')
        elif not id_exists.nextId():
            return redirect(f'{self.module_name}_with_id', id_exists.getPrevID())
        else:
            return redirect(f'{self.module_name}_with_id', id_exists.getNextID())

    def frm_move_first(self):
        if self.module_name == 'purchase' or self.module_name == 'sales':
            tbl = self.model.objects.filter(transaction_type = '').first()
        elif self.module_name == 'purchaseReturn' or self.module_name == 'salesReturn':
            tbl = self.model.objects.filter(transaction_type = 'return').first()
        else:
            tbl = self.model.objects.first()
        return redirect(f'{self.module_name}_with_id', tbl.id)
    
    
    def frm_move_previous(self):
        if self.module_name == 'purchase' or self.module_name == 'sales':
            tbl = self.model.objects.filter(transaction_type = '', id__lt=self.frm_id).order_by('-id').first()
        elif self.module_name == 'purchaseReturn' or self.module_name == 'salesReturn':
            tbl = self.model.objects.filter(transaction_type = 'return', id__lt=self.frm_id).order_by('-id').first()
        else:
            tbl = self.model.objects.filter(id__lt=self.frm_id).order_by('-id').first()
        return redirect(f'{self.module_name}_with_id', tbl.id)

    def frm_move_next(self):
        if self.module_name == 'purchase' or self.module_name == 'sales':
            tbl = self.model.objects.filter(transaction_type = '', id__gt=self.frm_id).order_by('id').first()
        elif self.module_name == 'purchaseReturn' or self.module_name == 'salesReturn':
            tbl = self.model.objects.filter(transaction_type = 'return', id__gt=self.frm_id).order_by('id').first()
        else:
            tbl = self.model.objects.filter(id__gt=self.frm_id).order_by('id').first()
        return redirect(f'{self.module_name}_with_id', tbl.id)

    def frm_move_last(self):
        if self.module_name == 'purchase' or self.module_name == 'sales':
            tbl = self.model.objects.filter(transaction_type = '').last()
        elif self.module_name == 'purchaseReturn' or self.module_name == 'salesReturn':
            tbl = self.model.objects.filter(transaction_type = 'return').last()
        else:
            tbl = self.model.objects.last()
        return redirect(f'{self.module_name}_with_id', tbl.id)
    
    def frm_find(self):
        if self.module_name == 'purchase' or self.module_name == 'sales':
            values = self.model.objects.filter(transaction_type = '')
        elif self.module_name == 'purchaseReturn' or self.module_name == 'salesReturn':
            values = self.model.objects.filter(transaction_type = 'return')
        else:
            values = self.model.objects.all()
        return render(self.request, self.list_template, {'values': values})