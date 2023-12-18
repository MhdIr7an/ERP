from django.apps import apps
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password

from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q
import json

from . frm import model_mapping
from . models import tblUsers, tblSales_Details, tblSales_Master, tblCustomer, tblPurchase_Master, tblPurchase_Details, tblVendor, tblProduct, tblProduct_unit, tblCategory, tblEmployee
from . rpt import invoice_print
from . convertions import to_decimal


def index(request):
    return redirect('home')

def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = tblUsers.objects.get(username=username)
        except tblUsers.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('login')
        
        
        user_login = authenticate(request, username=username, password=password)

        if user_login is not None:
            login(request, user_login)
            return redirect('home')
        else:
            messages.error(request, "Invalid password")
            request.session['data'] = { 'username' : username }
            return redirect('login')
        
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = {}

    return render(request, 'login.html', context)

def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if tblUsers.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            request.session['data'] = { 
            'username': username, 
            'email': email,
            }
            return redirect('register')
        if len(password) < 4 or len(password) > 10:
            messages.info(request, 'Password must be between 4 to 10 characters')
            request.session['data'] = { 
            'username': username,
            'email': email,
            }
            return redirect('register')
        else:
            hashed_password = make_password(password)
            x = tblUsers.objects.create(
                username=username,
                email=email,
                password=hashed_password, 
            )
            x.save()
            user_login = authenticate(request, username=username, password=password)

            if user_login is not None:
                login(request, user_login)
                # if user_login.user_type == 0:
                #     return redirect('organiser_requests')
                # elif user_login.user_type == 1:
                #     return redirect('volunteer')
                # elif user_login.user_type == 2:
                #     return redirect('organise_event')
                # elif user_login.user_type == 3:
                #     return redirect('orders')
                # elif user_login.user_type == 4:
                #     return redirect('publish_paper')            
                return redirect('home')
                
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = { }

    return render(request, 'register.html', context)

def logoutUser(request):
    logout(request)


#home
def homePage(request):
    return render(request, 'main/home.html')

def companyPage(request):
    return render(request, 'main/company.html')

def employeesPage(request):
    return render(request, 'main/employees.html')

def bankingPage(request):
    return render(request, 'main/banking.html')

def reportsPage(request):
    return render(request, 'main/reports.html')
    



#product
def product_view(request, frm_id=None):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_view()
    return result

def product_add(request):
    tbl = model_mapping(request, 'product', None)
    result = tbl.frm_add()
    return result

def product_edit(request, frm_id):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_edit()
    return result

def product_delete(request, frm_id):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_delete()
    return result

def product_move_first(request):
    tbl = model_mapping(request, 'product', None)
    result = tbl.frm_move_first()
    return result

def product_move_previous(request, frm_id):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_move_previous()
    return result

def product_move_next(request, frm_id):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_move_next()
    return result

def product_move_last(request):
    return redirect('product')

def product_find(request):
    tbl = model_mapping(request, 'product', None)
    result = tbl.frm_find()
    return result

def product_print(request):
    pass

#customer
def customer_view(request, frm_id=None):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_view()
    return result  # Return the rendered response

def customer_add(request):
    tbl = model_mapping(request, 'customer', None)
    result = tbl.frm_add()
    return result

def customer_edit(request, frm_id):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_edit()
    return result

def customer_delete(request, frm_id):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_delete()
    return result

def customer_move_first(request):
    tbl = model_mapping(request, 'customer', None)
    result = tbl.frm_move_first()
    return result

def customer_move_previous(request, frm_id):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_move_previous()
    return result

def customer_move_next(request, frm_id):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_move_next()
    return result

def customer_move_last(request):
    return redirect('customer')

def customer_find(request):
    tbl = model_mapping(request, 'customer', None)
    result = tbl.frm_find()
    return result

def customer_print(request):
    pass

#vendor
def vendor_view(request, frm_id=None):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_view()
    return result  # Return the rendered response

def vendor_add(request):
    tbl = model_mapping(request, 'vendor', None)
    result = tbl.frm_add()
    return result

def vendor_edit(request, frm_id):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_edit()
    return result

def vendor_delete(request, frm_id):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_delete()
    return result

def vendor_move_first(request):
    tbl = model_mapping(request, 'vendor', None)
    result = tbl.frm_move_first()
    return result

def vendor_move_previous(request, frm_id):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_move_previous()
    return result

def vendor_move_next(request, frm_id):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_move_next()
    return result

def vendor_move_last(request):
    return redirect('vendor')

def vendor_find(request):
    tbl = model_mapping(request, 'vendor', None)
    result = tbl.frm_find()
    return result

def vendor_print(request):
    pass


#category
def category_view(request, frm_id=None):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_view()
    return result  # Return the rendered response

def category_add(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_add()
    return result

def category_edit(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_edit()
    return result

def category_delete(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_delete()
    return result

def category_move_first(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_move_first()
    return result

def category_move_previous(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_move_previous()
    return result

def category_move_next(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_move_next()
    return result

def category_move_last(request):
    return redirect('category')

def category_find(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_find()
    return result

def category_print(request):
    pass


#currency
def currency_view(request, frm_id=None):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_view()
    return result  # Return the rendered response

def currency_add(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_add()
    return result

def currency_edit(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_edit()
    return result

def currency_delete(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_delete()
    return result

def currency_move_first(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_move_first()
    return result

def currency_move_previous(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_move_previous()
    return result

def currency_move_next(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_move_next()
    return result

def currency_move_last(request):
    return redirect('category')

def currency_find(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_find()
    return result

def currency_print(request):
    pass


def sales_view(request, frm_id=None):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_view()
    return result
    
def sales_add(request):
    tbl = model_mapping(request, 'sales', None)
    result = tbl.frm_add()
    return result

def sales_edit(request, frm_id):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
def sales_delete(request, frm_id):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_delete()
    return result

def sales_move_first(request):
    tbl = model_mapping(request, 'sales', None)
    result = tbl.frm_move_first()
    return result

def sales_move_previous(request, frm_id):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_move_previous()
    return result

def sales_move_next(request, frm_id):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_move_next()
    return result

def sales_move_last(request):
    return redirect('sales')

def sales_find(request):
    tbl = model_mapping(request, 'sales', None)
    result = tbl.frm_find()
    return result

def sales_print(request, frm_id):
    return invoice_print(request, frm_id, 'sales')

def purchase_view(request, frm_id=None):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_view()
    return result
    
def purchase_add(request):
    tbl = model_mapping(request, 'purchase', None)
    result = tbl.frm_add()
    return result

def purchase_edit(request, frm_id):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
def purchase_delete(request, frm_id):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_delete()
    return result

def purchase_move_first(request):
    tbl = model_mapping(request, 'purchase', None)
    result = tbl.frm_move_first()
    return result

def purchase_move_previous(request, frm_id):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_move_previous()
    return result

def purchase_move_next(request, frm_id):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_move_next()
    return result

def purchase_move_last(request):
    return redirect('purchase')

def purchase_find(request):
    tbl = model_mapping(request, 'purchase', None)
    result = tbl.frm_find()
    return result

def purchase_print(request, frm_id):
    return invoice_print(request, frm_id, 'purchase')


def salesReturn_view(request, frm_id=None):
    tbl = model_mapping(request, 'salesReturn', frm_id, True)
    result = tbl.frm_view()
    return result
    
def salesReturn_add(request):
    tbl = model_mapping(request, 'salesReturn', None, True)
    result = tbl.frm_add()
    return result

def salesReturn_edit(request, frm_id):
    tbl = model_mapping(request, 'salesReturn', frm_id, True)
    result = tbl.frm_edit()
    return result


@transaction.atomic
def salesReturn_delete(request, frm_id):
    tbl = model_mapping(request, 'salesReturn', frm_id, True)
    result = tbl.frm_delete()
    return result

def salesReturn_move_first(request):
    tbl = model_mapping(request, 'salesReturn', None, True)
    result = tbl.frm_move_first()
    return result

def salesReturn_move_previous(request, frm_id):
    tbl = model_mapping(request, 'salesReturn', frm_id, True)
    result = tbl.frm_move_previous()
    return result

def salesReturn_move_next(request, frm_id):
    tbl = model_mapping(request, 'salesReturn', frm_id, True)
    result = tbl.frm_move_next()
    return result

def salesReturn_move_last(request):
    return redirect('salesReturn')

def salesReturn_find(request):
    tbl = model_mapping(request, 'salesReturn', None, True)
    result = tbl.frm_find()
    return result

def salesReturn_print(request, frm_id):
    return invoice_print(request, frm_id, 'salesReturn')

def purchaseReturn_view(request, frm_id=None):
    tbl = model_mapping(request, 'purchaseReturn', frm_id, True)
    result = tbl.frm_view()
    return result
    
def purchaseReturn_add(request):
    tbl = model_mapping(request, 'purchaseReturn', None, True)
    result = tbl.frm_add()
    return result

def purchaseReturn_edit(request, frm_id):
    tbl = model_mapping(request, 'purchaseReturn', frm_id, True)
    result = tbl.frm_edit()
    return result


@transaction.atomic
def purchaseReturn_delete(request, frm_id):
    tbl = model_mapping(request, 'purchaseReturn', frm_id, True)
    result = tbl.frm_delete()
    return result

def purchaseReturn_move_first(request):
    tbl = model_mapping(request, 'purchaseReturn', None, True)
    result = tbl.frm_move_first()
    return result

def purchaseReturn_move_previous(request, frm_id):
    tbl = model_mapping(request, 'purchaseReturn', frm_id, True)
    result = tbl.frm_move_previous()
    return result

def purchaseReturn_move_next(request, frm_id):
    tbl = model_mapping(request, 'purchaseReturn', frm_id, True)
    result = tbl.frm_move_next()
    return result

def purchaseReturn_move_last(request):
    return redirect('purchaseReturn')

def purchaseReturn_find(request):
    tbl = model_mapping(request, 'purchaseReturn', None, True)
    result = tbl.frm_find()
    return result

def purchaseReturn_print(request, frm_id):
    return invoice_print(request, frm_id, 'purchaseReturn')


def salesOrder_view(request, frm_id=None):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_view()
    return result
    
def salesOrder_add(request):
    tbl = model_mapping(request, 'salesOrder', None)
    result = tbl.frm_add()
    return result

def salesOrder_edit(request, frm_id):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
def salesOrder_delete(request, frm_id):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_delete()
    return result

def salesOrder_move_first(request):
    tbl = model_mapping(request, 'salesOrder', None)
    result = tbl.frm_move_first()
    return result

def salesOrder_move_previous(request, frm_id):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_move_previous()
    return result

def salesOrder_move_next(request, frm_id):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_move_next()
    return result

def salesOrder_move_last(request):
    return redirect('salesOrder')

def salesOrder_find(request):
    tbl = model_mapping(request, 'salesOrder', None)
    result = tbl.frm_find()
    return result

def salesOrder_print(request, frm_id):
    return invoice_print(request, frm_id, 'salesOrder')

def purchaseOrder_view(request, frm_id=None):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_view()
    return result
    
def purchaseOrder_add(request):
    tbl = model_mapping(request, 'purchaseOrder', None)
    result = tbl.frm_add()
    return result

def purchaseOrder_edit(request, frm_id):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
def purchaseOrder_delete(request, frm_id):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_delete()
    return result

def purchaseOrder_move_first(request):
    tbl = model_mapping(request, 'purchaseOrder', None)
    result = tbl.frm_move_first()
    return result

def purchaseOrder_move_previous(request, frm_id):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_move_previous()
    return result

def purchaseOrder_move_next(request, frm_id):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_move_next()
    return result

def purchaseOrder_move_last(request):
    return redirect('purchaseOrder')

def purchaseOrder_find(request):
    tbl = model_mapping(request, 'purchaseOrder', None)
    result = tbl.frm_find()
    return result

def purchaseOrder_print(request, frm_id):
    return invoice_print(request, frm_id, 'purchaseOrder')












@transaction.atomic
def save_sales(request, sales_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))

            # Extract fieldValues and data from the dictionary
            master_data = data['master_data']
            details_data = data['details_data']
            # print(master_data, details_data)
            total = to_decimal(master_data[3])
            vat = to_decimal(master_data[4])
            discount = to_decimal(master_data[5])
            roundoff = to_decimal(master_data[6])
            net_amount = to_decimal(master_data[7])
            amount_received = to_decimal(master_data[8])
            balance = to_decimal(master_data[9])
            customer = tblCustomer.objects.get(id=master_data[11])
            salesman = tblEmployee.objects.get(id=master_data[12])
            if sales_id:
                sales = tblSales_Master.objects.get(id=sales_id)
                if (master_data[1] == ''):
                    customer.credit_balance = to_decimal(customer.credit_balance) - to_decimal(sales.balance)
                else:
                    customer.credit_balance = to_decimal(customer.credit_balance) + to_decimal(sales.balance)
                sales.invoice_no = master_data[0]
                sales.return_no = master_data[1]
                sales.invoice_date = master_data[2]
                sales.total = total
                sales.vat = vat
                sales.discount = discount
                sales.roundoff = roundoff
                sales.net_amount = net_amount
                sales.amount_received = amount_received
                sales.balance = balance
                sales.payment_method = master_data[10]
                sales.customer = customer
                sales.salesman = salesman
                sales.save()
                sales_details = tblSales_Details.objects.filter(sales = sales_id)
                for details in sales_details:
                    product = tblProduct.objects.get(id = details.product.id)
                    
                    if product.main_unit == details.unit:
                        multiple = 1
                    else:
                        prod_unit = tblProduct_unit.objects.get(product = product, unit = details.unit)
                        if prod_unit.multiple == '*':
                            multiple = 1/to_decimal(prod_unit.multiple_value)
                        else:
                            multiple = to_decimal(prod_unit.multiple_value)
                    if (master_data[1] == ''):
                        product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))+(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) + (to_decimal(details.qty)*multiple))
                        product.stock = to_decimal(product.stock) + (to_decimal(details.qty) * multiple)
                    else:
                        product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))-(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) - (to_decimal(details.qty)*multiple))
                        product.stock = to_decimal(product.stock) - (to_decimal(details.qty) * multiple)
                    product.save()
                sales_details.delete()
            else:
                sales = tblSales_Master.objects.create(
                    invoice_no = master_data[0],
                    return_no = master_data[1],
                    invoice_date = master_data[2],
                    total = total,
                    vat = vat,
                    discount = discount,
                    roundoff = roundoff,
                    net_amount = net_amount,
                    amount_received = amount_received,
                    balance = balance,
                    payment_method = master_data[10],
                    customer = customer,
                    salesman = salesman,
                    transaction_type = '' if master_data[1] == '' else 'return'
                )
            if (master_data[1] == ''):
                customer.credit_balance = to_decimal(customer.credit_balance) + balance
            else:
                customer.credit_balance = to_decimal(customer.credit_balance) - balance
            customer.save()

            for details in details_data:
                product = tblProduct.objects.get(id=details[2])
                unit = details[3]
                stock = to_decimal(details[4])
                qty = to_decimal(details[5])
                price = to_decimal(details[6])
                vat_perc = to_decimal(details[7])
                vat_amount = to_decimal(details[8])
                item_discount = to_decimal(details[9])
                total_amount = to_decimal(details[10])

                tblSales_Details.objects.create(
                    sales = sales,
                    product = product,
                    unit = unit,
                    stock = stock,
                    qty = qty,
                    price = price,
                    vat_perc = vat_perc,
                    vat_amount = vat_amount,
                    item_discount = item_discount,
                    total_amount = total_amount,
                )

                if product.main_unit == unit:
                    multiple = 1
                else:
                    prod_unit = tblProduct_unit.objects.get(product = product, unit = unit)
                    if prod_unit.multiple == '*':
                        multiple = 1/to_decimal(prod_unit.multiple_value)
                    else:
                        multiple = to_decimal(prod_unit.multiple_value)
                # print(multiple)
                # print(product.cost_price, product.stock, price, qty)
                # return
                if (master_data[1] == ''):
                    product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))-(price * qty))/(to_decimal(product.stock) - (qty * multiple))
                    product.stock = to_decimal(product.stock) - (qty * multiple)
                else:
                    product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))+(price * qty))/(to_decimal(product.stock) + (qty * multiple))
                    product.stock = to_decimal(product.stock) + (qty * multiple)
                product.save()



            return JsonResponse({'message': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'failed', 'error': 'Invalid JSON data'})
    else:
        return JsonResponse({'message': 'failed', 'error': 'Invalid request method'})
    


@transaction.atomic
def save_purchase(request, purchase_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))
            # Extract fieldValues and data from the dictionary
            master_data = data['master_data']
            details_data = data['details_data']
            # print(master_data, details_data)
            total = to_decimal(master_data[4])
            vat = to_decimal(master_data[5])
            discount = to_decimal(master_data[6])
            roundoff = to_decimal(master_data[7])
            net_amount = to_decimal(master_data[8])
            amount_payed = to_decimal(master_data[9])
            balance = to_decimal(master_data[10])
            vendor = tblVendor.objects.get(id=master_data[12])
            salesman = tblEmployee.objects.get(id=master_data[13])
            if purchase_id:
                purchase = tblPurchase_Master.objects.get(id=purchase_id)
                if (master_data[1] == ''):
                    vendor.credit_balance = to_decimal(vendor.credit_balance) - to_decimal(purchase.balance)
                else:
                    vendor.credit_balance = to_decimal(vendor.credit_balance) + to_decimal(purchase.balance)
                purchase.invoice_no = master_data[0]
                purchase.return_no = master_data[1]
                purchase.purchase_no = master_data[2]
                purchase.invoice_date = master_data[3]
                purchase.total = total
                purchase.vat = vat
                purchase.discount = discount
                purchase.roundoff = roundoff
                purchase.net_amount = net_amount
                purchase.amount_payed = amount_payed
                purchase.balance = balance
                purchase.payment_method = master_data[11]
                purchase.vendor = vendor
                purchase.salesman = salesman
                purchase.save()
                purchase_details = tblPurchase_Details.objects.filter(purchase = purchase_id)
                for details in purchase_details:
                    product = tblProduct.objects.get(id = details.product.id)
                    
                    if product.main_unit == details.unit:
                        multiple = 1
                    else:
                        prod_unit = tblProduct_unit.objects.get(product = product, unit = details.unit)
                        if prod_unit.multiple == '*':
                            multiple = 1/to_decimal(prod_unit.multiple_value)
                        else:
                            multiple = to_decimal(prod_unit.multiple_value)

                    if (master_data[1] == ''):
                        product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))-(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) - (to_decimal(details.qty)*multiple))
                        product.stock = to_decimal(product.stock) - (to_decimal(details.qty) * multiple)
                        product.last_purch_price = to_decimal(details.previous_purchase_price)
                    else:
                        product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))+(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) + (to_decimal(details.qty)*multiple))
                        product.stock = to_decimal(product.stock) + (to_decimal(details.qty) * multiple)
                    product.save()
                purchase_details.delete()
            else:
                purchase = tblPurchase_Master.objects.create(
                    invoice_no = master_data[0],
                    return_no = master_data[1],
                    purchase_no = master_data[2],
                    invoice_date = master_data[3],
                    total = total,
                    vat = vat,
                    discount = discount,
                    net_amount = net_amount,
                    amount_payed = amount_payed,
                    balance = balance,
                    roundoff = roundoff,
                    payment_method = master_data[11],
                    vendor = vendor,
                    salesman = salesman,
                    transaction_type = '' if master_data[1] == '' else 'return'
                )
            if (master_data[1] == ''):
                vendor.credit_balance = to_decimal(vendor.credit_balance) + balance
            else:
                vendor.credit_balance = to_decimal(vendor.credit_balance) - balance
            vendor.save()

            for details in details_data:
                product = tblProduct.objects.get(id=details[3])
                unit = details[4]
                qty = to_decimal(details[5])
                price = to_decimal(details[6])
                vat_perc = to_decimal(details[7])
                vat_amount = to_decimal(details[8])
                item_discount = to_decimal(details[9])
                total_amount = to_decimal(details[10])

                tblPurchase_Details.objects.create(
                    purchase = purchase,
                    product = product,
                    unit = unit,
                    qty = qty,
                    price = price,
                    vat_perc = vat_perc,
                    vat_amount = vat_amount,
                    item_discount = item_discount,
                    total_amount = total_amount,
                    previous_purchase_price = product.last_purch_price
                )
                
                if product.main_unit == unit:
                    multiple = 1
                else:
                    prod_unit = tblProduct_unit.objects.get(product = product, unit = unit)
                    if prod_unit.multiple == '*':
                        multiple = 1/to_decimal(prod_unit.multiple_value)
                    else:
                        multiple = to_decimal(prod_unit.multiple_value)
                # print(multiple)
                # print(product.cost_price, product.stock, price, qty)
                # return
                if (master_data[1] == ''):
                    product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))+(price * qty))/(to_decimal(product.stock) + (qty * multiple))
                    product.stock = to_decimal(product.stock) + (qty * multiple)
                    product.last_purch_price = price / multiple
                else:
                    product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))-(price * qty))/(to_decimal(product.stock) - (qty * multiple))
                    product.stock = to_decimal(product.stock) - (qty * multiple)
                product.save()




            return JsonResponse({'message': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'failed', 'error': 'Invalid JSON data'})
    else:
        return JsonResponse({'message': 'failed', 'error': 'Invalid request method'})



@transaction.atomic
def save_salesOrder(request, order_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))

            # Extract fieldValues and data from the dictionary
            master_data = data['master_data']
            details_data = data['details_data']
            # print(master_data, details_data)
            total = to_decimal(master_data[2])
            vat = to_decimal(master_data[3])
            discount = to_decimal(master_data[4])
            roundoff = to_decimal(master_data[5])
            net_amount = to_decimal(master_data[6])
            customer = tblCustomer.objects.get(id=master_data[7])
            salesman = tblEmployee.objects.get(id=master_data[8])
            if order_id:
                sales_order = tblSalesOrder_Master.objects.get(id=order_id)
                sales_order.order_no = master_data[0]
                sales_order.order_date = master_data[1]
                sales_order.total = total
                sales_order.vat = vat
                sales_order.discount = discount
                sales_order.roundoff = roundoff
                sales_order.net_amount = net_amount
                sales_order.customer = customer
                sales_order.salesman = salesman
                sales_order.save()
                salesOrder_details = tblSalesOrder_Details.objects.filter(sales_order = order_id)
                salesOrder_details.delete()
            else:
                sales_order = tblSalesOrder_Master.objects.create(
                    order_no = master_data[0],
                    order_date = master_data[1],
                    total = total,
                    vat = vat,
                    discount = discount,
                    roundoff = roundoff,
                    net_amount = net_amount,
                    customer = customer,
                    salesman = salesman,
                )

            for details in details_data:
                product = tblProduct.objects.get(id=details[2])
                unit = details[3]
                stock = to_decimal(details[4])
                qty = to_decimal(details[5])
                price = to_decimal(details[6])
                vat_perc = to_decimal(details[7])
                vat_amount = to_decimal(details[8])
                item_discount = to_decimal(details[9])
                total_amount = to_decimal(details[10])

                tblSalesOrder_Details.objects.create(
                    sales_order = sales_order,
                    product = product,
                    unit = unit,
                    stock = stock,
                    qty = qty,
                    price = price,
                    vat_perc = vat_perc,
                    vat_amount = vat_amount,
                    item_discount = item_discount,
                    total_amount = total_amount,
                )



            return JsonResponse({'message': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'failed', 'error': 'Invalid JSON data'})
    else:
        return JsonResponse({'message': 'failed', 'error': 'Invalid request method'})
    


@transaction.atomic
def save_purchaseOrder(request, purchase_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))
            # Extract fieldValues and data from the dictionary
            master_data = data['master_data']
            details_data = data['details_data']
            # print(master_data, details_data)
            total = to_decimal(master_data[4])
            vat = to_decimal(master_data[5])
            discount = to_decimal(master_data[6])
            roundoff = to_decimal(master_data[7])
            net_amount = to_decimal(master_data[8])
            amount_payed = to_decimal(master_data[9])
            balance = to_decimal(master_data[10])
            vendor = tblVendor.objects.get(id=master_data[12])
            salesman = tblEmployee.objects.get(id=master_data[13])
            if purchase_id:
                purchase = tblPurchase_Master.objects.get(id=purchase_id)
                if (master_data[1] == ''):
                    vendor.credit_balance = to_decimal(vendor.credit_balance) - to_decimal(purchase.balance)
                else:
                    vendor.credit_balance = to_decimal(vendor.credit_balance) + to_decimal(purchase.balance)
                purchase.invoice_no = master_data[0]
                purchase.return_no = master_data[1]
                purchase.purchase_no = master_data[2]
                purchase.invoice_date = master_data[3]
                purchase.total = total
                purchase.vat = vat
                purchase.discount = discount
                purchase.roundoff = roundoff
                purchase.net_amount = net_amount
                purchase.amount_payed = amount_payed
                purchase.balance = balance
                purchase.payment_method = master_data[11]
                purchase.vendor = vendor
                purchase.salesman = salesman
                purchase.save()
                purchase_details = tblPurchase_Details.objects.filter(purchase = purchase_id)
                for details in purchase_details:
                    product = tblProduct.objects.get(id = details.product.id)
                    
                    if product.main_unit == details.unit:
                        multiple = 1
                    else:
                        prod_unit = tblProduct_unit.objects.get(product = product, unit = details.unit)
                        if prod_unit.multiple == '*':
                            multiple = 1/to_decimal(prod_unit.multiple_value)
                        else:
                            multiple = to_decimal(prod_unit.multiple_value)

                    if (master_data[1] == ''):
                        product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))-(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) - (to_decimal(details.qty)*multiple))
                        product.stock = to_decimal(product.stock) - (to_decimal(details.qty) * multiple)
                        product.last_purch_price = to_decimal(details.previous_purchase_price)
                    else:
                        product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))+(to_decimal(details.price)*to_decimal(details.qty)))/(to_decimal(product.stock) + (to_decimal(details.qty)*multiple))
                        product.stock = to_decimal(product.stock) + (to_decimal(details.qty) * multiple)
                    product.save()
                purchase_details.delete()
            else:
                purchase = tblPurchase_Master.objects.create(
                    invoice_no = master_data[0],
                    return_no = master_data[1],
                    purchase_no = master_data[2],
                    invoice_date = master_data[3],
                    total = total,
                    vat = vat,
                    discount = discount,
                    net_amount = net_amount,
                    amount_payed = amount_payed,
                    balance = balance,
                    roundoff = roundoff,
                    payment_method = master_data[11],
                    vendor = vendor,
                    salesman = salesman,
                    transaction_type = '' if master_data[1] == '' else 'return'
                )
            if (master_data[1] == ''):
                vendor.credit_balance = to_decimal(vendor.credit_balance) + balance
            else:
                vendor.credit_balance = to_decimal(vendor.credit_balance) - balance
            vendor.save()

            for details in details_data:
                product = tblProduct.objects.get(id=details[3])
                unit = details[4]
                qty = to_decimal(details[5])
                price = to_decimal(details[6])
                vat_perc = to_decimal(details[7])
                vat_amount = to_decimal(details[8])
                item_discount = to_decimal(details[9])
                total_amount = to_decimal(details[10])

                tblPurchase_Details.objects.create(
                    purchase = purchase,
                    product = product,
                    unit = unit,
                    qty = qty,
                    price = price,
                    vat_perc = vat_perc,
                    vat_amount = vat_amount,
                    item_discount = item_discount,
                    total_amount = total_amount,
                    previous_purchase_price = product.last_purch_price
                )
                
                if product.main_unit == unit:
                    multiple = 1
                else:
                    prod_unit = tblProduct_unit.objects.get(product = product, unit = unit)
                    if prod_unit.multiple == '*':
                        multiple = 1/to_decimal(prod_unit.multiple_value)
                    else:
                        multiple = to_decimal(prod_unit.multiple_value)
                # print(multiple)
                # print(product.cost_price, product.stock, price, qty)
                # return
                if (master_data[1] == ''):
                    product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))+(price * qty))/(to_decimal(product.stock) + (qty * multiple))
                    product.stock = to_decimal(product.stock) + (qty * multiple)
                    product.last_purch_price = price / multiple
                else:
                    product.cost_price = ((to_decimal(product.cost_price)*to_decimal(product.stock))-(price * qty))/(to_decimal(product.stock) - (qty * multiple))
                    product.stock = to_decimal(product.stock) - (qty * multiple)
                product.save()




            return JsonResponse({'message': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'failed', 'error': 'Invalid JSON data'})
    else:
        return JsonResponse({'message': 'failed', 'error': 'Invalid request method'})


@transaction.atomic
def save_product(request, product_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))

            # Extract fieldValues and data from the dictionary
            product_data = data['product_data']
            unit_data = data['unit_data']
            # print(product_data, unit_data)
            if product_id:
                product = tblProduct.objects.get(id=product_id)
                product.product_code = product_data[0]
                product.product_name = product_data[1]
                product.main_unit = product_data[2]
                product.description = product_data[3]
                product.stock = to_decimal(product_data[4])
                product.cost_price = to_decimal(product_data[5])
                product.selling_price = to_decimal(product_data[6])
                product.vendor = tblVendor.objects.get(id = product_data[7])
                product.category = tblCategory.objects.get(id = product_data[8])
                product.save()
                sub_unit = tblProduct_unit.objects.filter(product = product_id)
                sub_unit.delete()
            else:
                product = tblProduct.objects.create(
                    product_code = product_data[0],
                    product_name = product_data[1],
                    main_unit = product_data[2],
                    description = product_data[3],
                    stock = to_decimal(product_data[4]),
                    cost_price = to_decimal(product_data[5]),
                    selling_price = to_decimal(product_data[6]),
                    vendor = tblVendor.objects.get(id = product_data[7]),
                    category = tblCategory.objects.get(id = product_data[8]),
                )



            for unit_value in unit_data:
                tblProduct_unit.objects.create(
                    product = product,
                    unit = str(unit_value[0]),
                    multiple = str(unit_value[1]),
                    multiple_value = to_decimal(str(unit_value[2])),
                )


            return JsonResponse({'message': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'failed', 'error': 'Invalid JSON data'})
    else:
        return JsonResponse({'message': 'failed', 'error': 'Invalid request method'})



def formSearch(request, tbl_name, tbl_field=None, field_code=None, tbl_field_2=None):
    try:
        model = apps.get_model(app_label='core', model_name=tbl_name)
        if tbl_field and field_code:
            filter_condition = Q(**{f"{tbl_field}__icontains": field_code})
            if tbl_field_2:
                filter_condition |= Q(**{f"{tbl_field_2}__icontains": field_code})
            results = model.objects.filter(filter_condition).values()
        elif field_code:
            if tbl_name == 'tblPurchase_Master':
                results = model.objects.filter(Q(vendor__vendor_name__icontains=field_code) | Q(invoice_no__icontains=field_code) | Q(purchase_no__icontains = field_code) | Q(return_no__icontains=field_code)).values()
            elif tbl_name == 'tblSales_Master':
                results = model.objects.filter(Q(customer__customer_name__icontains=field_code) | Q(invoice_no__icontains=field_code) | Q(return_no__icontains=field_code)).values()
            elif tbl_name == 'tblProduct':
                results = model.objects.filter(Q(vendor__vendor_name__icontains=field_code) | Q(category__category_name__icontains=field_code) | Q(product_name__icontains=field_code) | Q(product_code__icontains=field_code)).values()
            elif tbl_name == 'tblCustomer':
                results = model.objects.filter(Q(customer_code__icontains=field_code) | Q(customer_name__icontains=field_code) | Q(email__icontains=field_code) | Q(mobile__icontains=field_code)).values()
            elif tbl_name == 'tblVendor':
                results = model.objects.filter(Q(vendor_code__icontains=field_code) | Q(vendor_name__icontains=field_code) | Q(email__icontains=field_code) | Q(mobile__icontains=field_code)).values()
        else:
            results = model.objects.all().values()
        # Create a list to store the modified data
        data = []

        # Extract the 'fields' from each entry and add the 'id' field
        for result in results:
            if tbl_name == 'tblPurchase_Master':
                result['vendor_name'] = tblVendor.objects.get(id=result['vendor_id']).vendor_name
            elif tbl_name == 'tblSales_Master':
                result['customer_name'] = tblCustomer.objects.get(id=result['customer_id']).customer_name
            elif tbl_name == 'tblProduct':
                result['vendor_name'] = tblVendor.objects.get(id=result['vendor_id']).vendor_name
                result['category_name'] = tblCategory.objects.get(id=result['category_id']).category_name
                
            data.append(result)
        # Return the modified data as JSON response
        return JsonResponse(data, safe=False)

    except model.DoesNotExist:
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({})


def get_field_details(request, tbl_name, tbl_field, field_code, tbl_field_2=None):
    try:
        model = apps.get_model(app_label='core', model_name=tbl_name)

        if tbl_field_2:
            results = model.objects.filter(Q(**{tbl_field: field_code}) | Q(**{tbl_field_2: field_code})).values()
        else:
            results = model.objects.filter(**{tbl_field: field_code}).values()
        # Convert the queryset to a list of dictionaries
        results_list = list(results)

        return JsonResponse({'results': results_list} or {})
    except model.DoesNotExist:
        return JsonResponse({})
    except Exception as e:
        return JsonResponse({})


def does_field_exist(request, tbl_name, tbl_field, field_code):
    try:
        model = apps.get_model(app_label='core', model_name=tbl_name)
        if model.objects.filter(**{tbl_field: field_code}).exists():
            return JsonResponse({'result': "true"})
        else:
            return JsonResponse({})
    except:
        return JsonResponse({})