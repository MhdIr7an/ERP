from django.forms.models import model_to_dict
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction

from core.convertions import to_decimal


from .models import tblProduct, tblCustomer, tblProduct_unit, tblSales_Details, tblVendor, tblCategory, tblSales_Master, tblPurchase_Master, tblPurchase_Details
from .forms import ProductForm, CustomerForm, VendorForm, CategoryForm, SalesForm, PurchaseForm


class idExists:
    """
    Checks if next or previous id exists using current id
    """
    def __init__(self, tbl, frm_id, module_name, to_return=False):
        self.tbl = tbl
        self.frm_id = frm_id
        self.to_return = to_return
        self.module_name = module_name
    def nextId(self):
        filter_condition = {'id__gt': self.frm_id}
        if self.module_name == 'sales' or self.module_name == 'purchase' or self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
            if self.to_return:
                filter_condition['transaction_type'] = 'return'
            else: 
                filter_condition['return_no'] = 0        
        nxt = self.tbl.objects.filter(**filter_condition).order_by('id').first()
        return bool(nxt)

    def prevId(self):
        filter_condition = {'id__lt': self.frm_id}
        if self.module_name == 'sales' or self.module_name == 'purchase' or self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
            if self.to_return:
                filter_condition['transaction_type'] = 'return'
            else: 
                filter_condition['return_no'] = 0        
        prev = self.tbl.objects.filter(**filter_condition).order_by('-id').first()
        return bool(prev)

    
    def getNextID(self):
        filter_condition = {'id__gt': self.frm_id}
        if self.module_name == 'sales' or self.module_name == 'purchase' or self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
            if self.to_return:
                filter_condition['transaction_type'] = 'return'
            else: 
                filter_condition['return_no'] = 0
        nxt = self.tbl.objects.filter(**filter_condition).order_by('id').first()
        return model_to_dict(nxt)['id']

    def getPrevID(self):
        filter_condition = {'id__lt': self.frm_id}
        if self.module_name == 'sales' or self.module_name == 'purchase' or self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
            if self.to_return:
                filter_condition['transaction_type'] = 'return'
            else: 
                filter_condition['return_no'] = 0

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
    def __init__(self, request, module_name: str, frm_id=None, to_return=False):
        models = {
            "product": (tblProduct, ProductForm, 'product/view.html', 'product/add.html', 'product/edit.html', 'product/list.html'),
            "customer": (tblCustomer, CustomerForm, 'customer/view.html', 'customer/add.html', 'customer/edit.html', 'customer/list.html'),
            "vendor": (tblVendor, VendorForm, 'vendor/view.html', 'vendor/add.html', 'vendor/edit.html', 'vendor/list.html'),
            "category": (tblCategory, CategoryForm, 'category/view.html', 'category/add.html', 'category/edit.html', 'category/list.html'),
            "sales": (tblSales_Master, SalesForm, 'sales/view.html', 'sales/add.html', 'sales/edit.html', 'sales/list.html'),
            "purchase": (tblPurchase_Master, PurchaseForm, 'purchase/view.html', 'purchase/add.html', 'purchase/edit.html', 'purchase/list.html'),
            "salesReturn": (tblSales_Master, SalesForm, 'salesReturn/view.html', 'salesReturn/add.html', 'salesReturn/edit.html', 'salesReturn/list.html'),
            "purchaseReturn": (tblPurchase_Master, PurchaseForm, 'purchaseReturn/view.html', 'purchaseReturn/add.html', 'purchaseReturn/edit.html', 'purchaseReturn/list.html'),
        }
        self.module_name = module_name
        self.frm_id = frm_id
        self.request = request
        self.to_return = to_return
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

        find_checker = idExists(self.model, tbl.id, self.module_name, self.to_return)

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
        return render(self.request, self.view_template, context)

    @transaction.atomic
    def frm_add(self):
        """
        Add a form.
        """

        if self.request.method == 'POST':
            if self.module_name == 'product' or self.module_name == 'sales' or self.module_name == 'purchase' or self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
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
            if self.module_name == 'product' or self.module_name == 'sales'  or self.module_name == 'purchase' or self.module_name == 'salesReturn' or self.module_name == 'purchaseReturn':
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
        else:
            context.update({'id': self.frm_id})
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
        tbl.delete()
        id_exists = idExists(self.model, self.frm_id, self.module_name, self.to_return)
        if not id_exists.findId():
            return redirect(f'{self.module_name}_add')
        elif not id_exists.nextId():
            return redirect(f'{self.module_name}_with_id', id_exists.getPrevID())
        else:
            return redirect(f'{self.module_name}_with_id', id_exists.getNextID())

    def frm_move_first(self):
        tbl = self.model.objects.first()
        return redirect(f'{self.module_name}_with_id', tbl.id)
    
    
    def frm_move_previous(self):
        tbl = self.model.objects.filter(id__lt=self.frm_id).order_by('-id').first()
        return redirect(f'{self.module_name}_with_id', tbl.id)

    def frm_move_next(self):
        tbl = self.model.objects.filter(id__gt=self.frm_id).order_by('id').first()
        return redirect(f'{self.module_name}_with_id', tbl.id)
    
    def frm_find(self):
        if self.module_name == 'purchase' or self.module_name == 'sales':
            values = self.model.objects.filter(transaction_type = '')
        elif self.module_name == 'purchaseReturn' or self.module_name == 'salesReturn':
            values = self.model.objects.filter(transaction_type = 'return')
        else:
            values = self.model.objects.all()
        return render(self.request, self.list_template, {'values': values})

# def autocomplete_suggestions(request):
#     query = request.GET.get('query', '')
#     suggestions = tblCustomer.objects.filter(Q(customer_name__icontains=query) | Q(price__icontains=query))[:10]  # Adjust the filter conditions as needed
#     suggestions = [s.customer_name for s in suggestions]
#     return JsonResponse(suggestions, safe=False)

# def customer_json(request):
#     search_query = request.GET.get('search_query')
#     customers = tblCustomer.objects.filter(customer_name__icontains=search_query)
#     customers_list = list(customers.values())
#     for customer in customers_list:
#         customer['price'] = customer['price'].to_eng_string()
#     return JsonResponse(json.dumps(customers_list), safe=False)