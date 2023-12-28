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
from . models import (tblUsers, tblSales_Details, tblSales_Master, tblCustomer, tblPurchase_Master, tblPurchase_Details, tblVendor, tblSalesman, 
tblProduct, tblProduct_unit, tblCategory, tblSalesOrder_Master, tblSalesOrder_Details, tblPurchaseOrder_Master, tblPurchaseOrder_Details,
tblQuotation_Master, tblQuotation_Details, tblDeliveryNote_Master, 
tblDeliveryNote_Details, tblPayment, tblReceipt)
from . rpt import invoice_print
from . convertions import to_decimal

@login_required(login_url='/login')
def index(request):
    return redirect('home')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
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
    if request.user.is_authenticated:
        return redirect('index')
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
                return redirect('home')
                
    if request.session.get('data'):
        context = request.session.get('data')
        del request.session['data']
    else:
        context = { }

    return render(request, 'register.html', context)

@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('login')


#home
@login_required(login_url='/login')
def homePage(request):
    return render(request, 'main/home.html')
    



#product
@login_required(login_url='/login')
def product_view(request, frm_id=None):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_view()
    return result

@login_required(login_url='/login')
def product_add(request):
    tbl = model_mapping(request, 'product', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def product_edit(request, frm_id):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_edit()
    return result

@login_required(login_url='/login')
def product_delete(request, frm_id):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def product_move_first(request):
    tbl = model_mapping(request, 'product', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def product_move_previous(request, frm_id):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def product_move_next(request, frm_id):
    tbl = model_mapping(request, 'product', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def product_move_last(request):
    tbl = model_mapping(request, 'product', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def product_find(request):
    tbl = model_mapping(request, 'product', None)
    result = tbl.frm_find()
    return result

#customer
@login_required(login_url='/login')
def customer_view(request, frm_id=None):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_view()
    return result  # Return the rendered response

@login_required(login_url='/login')
def customer_add(request):
    tbl = model_mapping(request, 'customer', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def customer_edit(request, frm_id):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_edit()
    return result

@login_required(login_url='/login')
def customer_delete(request, frm_id):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def customer_move_first(request):
    tbl = model_mapping(request, 'customer', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def customer_move_previous(request, frm_id):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def customer_move_next(request, frm_id):
    tbl = model_mapping(request, 'customer', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def customer_move_last(request):
    tbl = model_mapping(request, 'customer', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def customer_find(request):
    tbl = model_mapping(request, 'customer', None)
    result = tbl.frm_find()
    return result

#vendor
@login_required(login_url='/login')
def vendor_view(request, frm_id=None):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_view()
    return result  # Return the rendered response

@login_required(login_url='/login')
def vendor_add(request):
    tbl = model_mapping(request, 'vendor', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def vendor_edit(request, frm_id):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_edit()
    return result

@login_required(login_url='/login')
def vendor_delete(request, frm_id):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def vendor_move_first(request):
    tbl = model_mapping(request, 'vendor', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def vendor_move_previous(request, frm_id):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def vendor_move_next(request, frm_id):
    tbl = model_mapping(request, 'vendor', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def vendor_move_last(request):
    tbl = model_mapping(request, 'vendor', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def vendor_find(request):
    tbl = model_mapping(request, 'vendor', None)
    result = tbl.frm_find()
    return result


#category
@login_required(login_url='/login')
def category_view(request, frm_id=None):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_view()
    return result  # Return the rendered response

@login_required(login_url='/login')
def category_add(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def category_edit(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_edit()
    return result

@login_required(login_url='/login')
def category_delete(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def category_move_first(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def category_move_previous(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def category_move_next(request, frm_id):
    tbl = model_mapping(request, 'category', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def category_move_last(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def category_find(request):
    tbl = model_mapping(request, 'category', None)
    result = tbl.frm_find()
    return result

#salesman
@login_required(login_url='/login')
def salesman_view(request, frm_id=None):
    tbl = model_mapping(request, 'salesman', frm_id)
    result = tbl.frm_view()
    return result  # Return the rendered response

@login_required(login_url='/login')
def salesman_add(request):
    tbl = model_mapping(request, 'salesman', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def salesman_edit(request, frm_id):
    tbl = model_mapping(request, 'salesman', frm_id)
    result = tbl.frm_edit()
    return result

@login_required(login_url='/login')
def salesman_delete(request, frm_id):
    tbl = model_mapping(request, 'salesman', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def salesman_move_first(request):
    tbl = model_mapping(request, 'salesman', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def salesman_move_previous(request, frm_id):
    tbl = model_mapping(request, 'salesman', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def salesman_move_next(request, frm_id):
    tbl = model_mapping(request, 'salesman', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def salesman_move_last(request):
    tbl = model_mapping(request, 'salesman', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def salesman_find(request):
    tbl = model_mapping(request, 'salesman', None)
    result = tbl.frm_find()
    return result


@login_required(login_url='/login')
def sales_view(request, frm_id=None):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def sales_add(request):
    tbl = model_mapping(request, 'sales', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def sales_edit(request, frm_id):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def sales_delete(request, frm_id):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def sales_move_first(request):
    tbl = model_mapping(request, 'sales', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def sales_move_previous(request, frm_id):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def sales_move_next(request, frm_id):
    tbl = model_mapping(request, 'sales', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def sales_move_last(request):
    tbl = model_mapping(request, 'sales', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def sales_find(request):
    tbl = model_mapping(request, 'sales', None)
    result = tbl.frm_find()
    return result

@login_required(login_url='/login')
def sales_print(request, frm_id):
    return invoice_print(request, frm_id, 'sales')

@login_required(login_url='/login')
def purchase_view(request, frm_id=None):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def purchase_add(request):
    tbl = model_mapping(request, 'purchase', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def purchase_edit(request, frm_id):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def purchase_delete(request, frm_id):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def purchase_move_first(request):
    tbl = model_mapping(request, 'purchase', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def purchase_move_previous(request, frm_id):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def purchase_move_next(request, frm_id):
    tbl = model_mapping(request, 'purchase', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def purchase_move_last(request):
    tbl = model_mapping(request, 'purchase', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def purchase_find(request):
    tbl = model_mapping(request, 'purchase', None)
    result = tbl.frm_find()
    return result

@login_required(login_url='/login')
def purchase_print(request, frm_id):
    return invoice_print(request, frm_id, 'purchase')


@login_required(login_url='/login')
def salesReturn_view(request, frm_id=None):
    tbl = model_mapping(request, 'salesReturn', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def salesReturn_add(request):
    tbl = model_mapping(request, 'salesReturn', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def salesReturn_edit(request, frm_id):
    tbl = model_mapping(request, 'salesReturn', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def salesReturn_delete(request, frm_id):
    tbl = model_mapping(request, 'salesReturn', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def salesReturn_move_first(request):
    tbl = model_mapping(request, 'salesReturn', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def salesReturn_move_previous(request, frm_id):
    tbl = model_mapping(request, 'salesReturn', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def salesReturn_move_next(request, frm_id):
    tbl = model_mapping(request, 'salesReturn', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def salesReturn_move_last(request):
    tbl = model_mapping(request, 'salesReturn', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def salesReturn_find(request):
    tbl = model_mapping(request, 'salesReturn', None)
    result = tbl.frm_find()
    return result

@login_required(login_url='/login')
def salesReturn_print(request, frm_id):
    return invoice_print(request, frm_id, 'salesReturn')

@login_required(login_url='/login')
def purchaseReturn_view(request, frm_id=None):
    tbl = model_mapping(request, 'purchaseReturn', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def purchaseReturn_add(request):
    tbl = model_mapping(request, 'purchaseReturn', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def purchaseReturn_edit(request, frm_id):
    tbl = model_mapping(request, 'purchaseReturn', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def purchaseReturn_delete(request, frm_id):
    tbl = model_mapping(request, 'purchaseReturn', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def purchaseReturn_move_first(request):
    tbl = model_mapping(request, 'purchaseReturn', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def purchaseReturn_move_previous(request, frm_id):
    tbl = model_mapping(request, 'purchaseReturn', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def purchaseReturn_move_next(request, frm_id):
    tbl = model_mapping(request, 'purchaseReturn', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def purchaseReturn_move_last(request):
    tbl = model_mapping(request, 'purchaseReturn', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def purchaseReturn_find(request):
    tbl = model_mapping(request, 'purchaseReturn', None)
    result = tbl.frm_find()
    return result

@login_required(login_url='/login')
def purchaseReturn_print(request, frm_id):
    return invoice_print(request, frm_id, 'purchaseReturn')


@login_required(login_url='/login')
def salesOrder_view(request, frm_id=None):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def salesOrder_add(request):
    tbl = model_mapping(request, 'salesOrder', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def salesOrder_edit(request, frm_id):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def salesOrder_delete(request, frm_id):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def salesOrder_move_first(request):
    tbl = model_mapping(request, 'salesOrder', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def salesOrder_move_previous(request, frm_id):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def salesOrder_move_next(request, frm_id):
    tbl = model_mapping(request, 'salesOrder', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def salesOrder_move_last(request):
    tbl = model_mapping(request, 'salesOrder', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def salesOrder_find(request):
    tbl = model_mapping(request, 'salesOrder', None)
    result = tbl.frm_find()
    return result

@login_required(login_url='/login')
def salesOrder_print(request, frm_id):
    return invoice_print(request, frm_id, 'salesOrder')


@login_required(login_url='/login')
def purchaseOrder_view(request, frm_id=None):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def purchaseOrder_add(request):
    tbl = model_mapping(request, 'purchaseOrder', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def purchaseOrder_edit(request, frm_id):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def purchaseOrder_delete(request, frm_id):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def purchaseOrder_move_first(request):
    tbl = model_mapping(request, 'purchaseOrder', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def purchaseOrder_move_previous(request, frm_id):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def purchaseOrder_move_next(request, frm_id):
    tbl = model_mapping(request, 'purchaseOrder', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def purchaseOrder_move_last(request):
    tbl = model_mapping(request, 'purchaseOrder', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def purchaseOrder_find(request):
    tbl = model_mapping(request, 'purchaseOrder', None)
    result = tbl.frm_find()
    return result

@login_required(login_url='/login')
def purchaseOrder_print(request, frm_id):
    return invoice_print(request, frm_id, 'purchaseOrder')


@login_required(login_url='/login')
def deliveryNote_view(request, frm_id=None):
    tbl = model_mapping(request, 'deliveryNote', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def deliveryNote_add(request):
    tbl = model_mapping(request, 'deliveryNote', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def deliveryNote_edit(request, frm_id):
    tbl = model_mapping(request, 'deliveryNote', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def deliveryNote_delete(request, frm_id):
    tbl = model_mapping(request, 'deliveryNote', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def deliveryNote_move_first(request):
    tbl = model_mapping(request, 'deliveryNote', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def deliveryNote_move_previous(request, frm_id):
    tbl = model_mapping(request, 'deliveryNote', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def deliveryNote_move_next(request, frm_id):
    tbl = model_mapping(request, 'deliveryNote', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def deliveryNote_move_last(request):
    tbl = model_mapping(request, 'deliveryNote', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def deliveryNote_find(request):
    tbl = model_mapping(request, 'deliveryNote', None)
    result = tbl.frm_find()
    return result

@login_required(login_url='/login')
def deliveryNote_print(request, frm_id):
    return invoice_print(request, frm_id, 'deliveryNote')


@login_required(login_url='/login')
def quotation_view(request, frm_id=None):
    tbl = model_mapping(request, 'quotation', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def quotation_add(request):
    tbl = model_mapping(request, 'quotation', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def quotation_edit(request, frm_id):
    tbl = model_mapping(request, 'quotation', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def quotation_delete(request, frm_id):
    tbl = model_mapping(request, 'quotation', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def quotation_move_first(request):
    tbl = model_mapping(request, 'quotation', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def quotation_move_previous(request, frm_id):
    tbl = model_mapping(request, 'quotation', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def quotation_move_next(request, frm_id):
    tbl = model_mapping(request, 'quotation', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def quotation_move_last(request):
    tbl = model_mapping(request, 'quotation', None)
    result = tbl.frm_move_last()
    return result


@login_required(login_url='/login')
def quotation_find(request):
    tbl = model_mapping(request, 'quotation', None)
    result = tbl.frm_find()
    return result

@login_required(login_url='/login')
def quotation_print(request, frm_id):
    return invoice_print(request, frm_id, 'quotation')


@login_required(login_url='/login')
def payment_view(request, frm_id=None):
    tbl = model_mapping(request, 'payment', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def payment_add(request):
    tbl = model_mapping(request, 'payment', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def payment_edit(request, frm_id):
    tbl = model_mapping(request, 'payment', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def payment_delete(request, frm_id):
    tbl = model_mapping(request, 'payment', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def payment_move_first(request):
    tbl = model_mapping(request, 'payment', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def payment_move_previous(request, frm_id):
    tbl = model_mapping(request, 'payment', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def payment_move_next(request, frm_id):
    tbl = model_mapping(request, 'payment', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def payment_move_last(request):
    tbl = model_mapping(request, 'payment', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def payment_find(request):
    tbl = model_mapping(request, 'payment', None)
    result = tbl.frm_find()
    return result


@login_required(login_url='/login')
def receipt_view(request, frm_id=None):
    tbl = model_mapping(request, 'receipt', frm_id)
    result = tbl.frm_view()
    return result
    
@login_required(login_url='/login')
def receipt_add(request):
    tbl = model_mapping(request, 'receipt', None)
    result = tbl.frm_add()
    return result

@login_required(login_url='/login')
def receipt_edit(request, frm_id):
    tbl = model_mapping(request, 'receipt', frm_id)
    result = tbl.frm_edit()
    return result


@transaction.atomic
@login_required(login_url='/login')
def receipt_delete(request, frm_id):
    tbl = model_mapping(request, 'receipt', frm_id)
    result = tbl.frm_delete()
    return result

@login_required(login_url='/login')
def receipt_move_first(request):
    tbl = model_mapping(request, 'receipt', None)
    result = tbl.frm_move_first()
    return result

@login_required(login_url='/login')
def receipt_move_previous(request, frm_id):
    tbl = model_mapping(request, 'receipt', frm_id)
    result = tbl.frm_move_previous()
    return result

@login_required(login_url='/login')
def receipt_move_next(request, frm_id):
    tbl = model_mapping(request, 'receipt', frm_id)
    result = tbl.frm_move_next()
    return result

@login_required(login_url='/login')
def receipt_move_last(request):
    tbl = model_mapping(request, 'receipt', None)
    result = tbl.frm_move_last()
    return result

@login_required(login_url='/login')
def receipt_find(request):
    tbl = model_mapping(request, 'receipt', None)
    result = tbl.frm_find()
    return result











@transaction.atomic
@login_required(login_url='/login')
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
            salesman = tblSalesman.objects.get(id=master_data[12])
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
@login_required(login_url='/login')
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
            salesman = tblSalesman.objects.get(id=master_data[13])
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
                product = tblProduct.objects.get(id=details[2])
                unit = details[3]
                qty = to_decimal(details[4])
                price = to_decimal(details[5])
                vat_perc = to_decimal(details[6])
                vat_amount = to_decimal(details[7])
                item_discount = to_decimal(details[8])
                total_amount = to_decimal(details[9])

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
@login_required(login_url='/login')
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


@transaction.atomic
@login_required(login_url='/login')
def save_salesOrder(request, order_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))

            # Extract fieldValues and data from the dictionary
            master_data = data['master_data']
            details_data = data['details_data']
            print(master_data, details_data)
            total = to_decimal(master_data[2])
            vat = to_decimal(master_data[3])
            discount = to_decimal(master_data[4])
            roundoff = to_decimal(master_data[5])
            net_amount = to_decimal(master_data[6])
            customer = tblCustomer.objects.get(id=master_data[7])
            salesman = tblSalesman.objects.get(id=master_data[8])
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
@login_required(login_url='/login')
def save_purchaseOrder(request, order_id=None):
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
            vendor = tblVendor.objects.get(id=master_data[7])
            salesman = tblSalesman.objects.get(id=master_data[8])
            if order_id:
                purchase_order = tblPurchaseOrder_Master.objects.get(id=order_id)
                purchase_order.order_no = master_data[0]
                purchase_order.order_date = master_data[1]
                purchase_order.total = total
                purchase_order.vat = vat
                purchase_order.discount = discount
                purchase_order.roundoff = roundoff
                purchase_order.net_amount = net_amount
                purchase_order.vendor = vendor
                purchase_order.salesman = salesman
                purchase_order.save()
                purchase_order_details = tblPurchaseOrder_Details.objects.filter(purchase_order = order_id)
                purchase_order_details.delete()
            else:
                purchase_order = tblPurchaseOrder_Master.objects.create(
                    order_no = master_data[0],
                    order_date = master_data[1],
                    total = total,
                    vat = vat,
                    discount = discount,
                    roundoff = roundoff,
                    net_amount = net_amount,
                    vendor = vendor,
                    salesman = salesman,
                )

            for details in details_data:
                product = tblProduct.objects.get(id=details[2])
                unit = details[3]
                qty = to_decimal(details[4])
                price = to_decimal(details[5])
                vat_perc = to_decimal(details[6])
                vat_amount = to_decimal(details[7])
                item_discount = to_decimal(details[8])
                total_amount = to_decimal(details[9])

                tblPurchaseOrder_Details.objects.create(
                    purchase_order = purchase_order,
                    product = product,
                    unit = unit,
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
@login_required(login_url='/login')
def save_quotation(request, quotation_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))
            # Extract fieldValues and data from the dictionary
            master_data = data['master_data']
            details_data = data['details_data']
            # print(master_data, details_data)
            total = to_decimal(master_data[2])
            discount = to_decimal(master_data[3])
            vat = to_decimal(master_data[4])
            roundoff = to_decimal(master_data[5])
            net_amount = to_decimal(master_data[6])
            customer = tblCustomer.objects.get(id=master_data[7])
            salesman = tblSalesman.objects.get(id=master_data[8])
            if quotation_id:
                quotation = tblQuotation_Master.objects.get(id=quotation_id)
                quotation.quotation_no = master_data[0]
                quotation.quotation_date = master_data[1]
                quotation.total = total
                quotation.discount = discount
                quotation.vat = vat
                quotation.roundoff = roundoff
                quotation.net_amount = net_amount
                quotation.customer = customer
                quotation.salesman = salesman
                quotation.save()
                quotation_details = tblQuotation_Details.objects.filter(quotation = quotation_id)
                quotation_details.delete()
            else:
                quotation = tblQuotation_Master.objects.create(
                    quotation_no = master_data[0],
                    quotation_date = master_data[1],
                    total = total,
                    discount = discount,
                    vat = vat,
                    roundoff = roundoff,
                    net_amount = net_amount,
                    customer = customer,
                    salesman = salesman,
                )

            for details in details_data:
                product = tblProduct.objects.get(id=details[0])
                unit = details[1]
                qty = to_decimal(details[2])
                price = to_decimal(details[3])
                vat_perc = to_decimal(details[4])
                vat_amount = to_decimal(details[5])
                item_discount = to_decimal(details[6])
                total_amount = to_decimal(details[7])

                tblQuotation_Details.objects.create(
                    quotation = quotation,
                    product = product,
                    unit = unit,
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
@login_required(login_url='/login')
def save_deliveryNote(request, deliveryNote_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))
            # Extract fieldValues and data from the dictionary
            master_data = data['master_data']
            details_data = data['details_data']
            # print(master_data, details_data)
            total = to_decimal(master_data[2])
            discount = to_decimal(master_data[3])
            vat = to_decimal(master_data[4])
            roundoff = to_decimal(master_data[5])
            net_amount = to_decimal(master_data[6])
            customer = tblCustomer.objects.get(id=master_data[7])
            salesman = tblSalesman.objects.get(id=master_data[8])
            if deliveryNote_id:
                deliveryNote = tblDeliveryNote_Master.objects.get(id=deliveryNote_id)
                deliveryNote.delivery_note_no = master_data[0]
                deliveryNote.delivery_note_date = master_data[1]
                deliveryNote.total = total
                deliveryNote.discount = discount
                deliveryNote.vat = vat
                deliveryNote.roundoff = roundoff
                deliveryNote.net_amount = net_amount
                deliveryNote.customer = customer
                deliveryNote.salesman = salesman
                deliveryNote.save()
                deliveryNote_details = tblDeliveryNote_Details.objects.filter(delivery_note = deliveryNote_id)
                deliveryNote_details.delete()
            else:
                deliveryNote = tblDeliveryNote_Master.objects.create(
                    delivery_note_no = master_data[0],
                    delivery_note_date = master_data[1],
                    total = total,
                    discount = discount,
                    vat = vat,
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

                tblDeliveryNote_Details.objects.create(
                    delivery_note = deliveryNote,
                    product = product,
                    unit = unit,
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
@login_required(login_url='/login')
def save_payment(request, payment_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))
            vendor = tblVendor.objects.get(id = data[2]) if data[2] is not '' else None
            if payment_id:
                payment = tblPayment.objects.get(id=payment_id)
                if vendor:
                    vendor.credit_balance = to_decimal(vendor.credit_balance) + to_decimal(payment.amount) + to_decimal(payment.discount)
                payment.payment_no = data[0]
                payment.payment_date = data[1]
                payment.vendor = vendor
                payment.payment_to = data[3]
                payment.amount = to_decimal(data[4])
                payment.discount = to_decimal(data[5])
                payment.payment_method = data[6]
                payment.save()
            else:
                payment = tblPayment.objects.create(
                    payment_no = data[0],
                    payment_date = data[1],
                    vendor = vendor,
                    payment_to = data[3],
                    amount = to_decimal(data[4]),
                    discount = to_decimal(data[5]),
                    payment_method = data[6],
                )
            if vendor:
                vendor.credit_balance = to_decimal(vendor.credit_balance) - to_decimal(data[3]) - to_decimal(data[4])
                vendor.save()

            return JsonResponse({'message': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'failed', 'error': 'Invalid JSON data'})
    else:
        return JsonResponse({'message': 'failed', 'error': 'Invalid request method'})



@transaction.atomic
@login_required(login_url='/login')
def save_receipt(request, receipt_id=None):
    if request.method == 'POST':
        try:
            # Get the data as a JSON string and parse it into a Python dictionary
            data = json.loads(request.body.decode('utf-8'))

            customer = tblCustomer.objects.get(id = data[2]) if data[2] is not '' else None
            if receipt_id:
                receipt = tblReceipt.objects.get(id=receipt_id)
                if customer:
                    customer.credit_balance = to_decimal(customer.credit_balance) + to_decimal(receipt.amount) + to_decimal(receipt.discount)
                receipt.receipt_no = data[0]
                receipt.receipt_date = data[1]
                receipt.customer = customer
                receipt.receipt_from = data[3]
                receipt.amount = to_decimal(data[4])
                receipt.discount = to_decimal(data[5])
                receipt.receipt_method = data[6]
                receipt.save()
            else:
                receipt = tblReceipt.objects.create(
                    receipt_no = data[0],
                    receipt_date = data[1],
                    customer = customer,
                    receipt_from = data[3],
                    amount = to_decimal(data[4]),
                    discount = to_decimal(data[5]),
                    payment_method = data[6],
                )
            if customer:
                customer.credit_balance = to_decimal(customer.credit_balance) - to_decimal(data[3]) - to_decimal(data[4])
                customer.save()

            return JsonResponse({'message': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'message': 'failed', 'error': 'Invalid JSON data'})
    else:
        return JsonResponse({'message': 'failed', 'error': 'Invalid request method'})


@login_required(login_url='/login')
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
            elif tbl_name == 'tblCategory':
                results = model.objects.filter(Q(category_code__icontains=field_code) | Q(category_name__icontains=field_code) | Q(vat_rate__icontains=field_code) | Q(type__icontains=field_code)).values()
            elif tbl_name == 'tblProduct':
                results = model.objects.filter(Q(vendor__vendor_name__icontains=field_code) | Q(category__category_name__icontains=field_code) | Q(product_name__icontains=field_code) | Q(product_code__icontains=field_code)).values()
            elif tbl_name == 'tblCustomer':
                results = model.objects.filter(Q(customer_code__icontains=field_code) | Q(customer_name__icontains=field_code) | Q(email__icontains=field_code) | Q(mobile__icontains=field_code)).values()
            elif tbl_name == 'tblVendor':
                results = model.objects.filter(Q(vendor_code__icontains=field_code) | Q(vendor_name__icontains=field_code) | Q(email__icontains=field_code) | Q(mobile__icontains=field_code)).values()
            elif tbl_name == 'tblSalesman':
                results = model.objects.filter(Q(salesman_code__icontains=field_code) | Q(salesman_name__icontains=field_code) | Q(email__icontains=field_code) | Q(mobile__icontains=field_code)).values()
            elif tbl_name == 'tblPurchaseOrder_Master':
                results = model.objects.filter(Q(vendor__vendor_name__icontains=field_code) | Q(order_no__icontains=field_code)).values()
            elif tbl_name == 'tblSalesOrder_Master':
                results = model.objects.filter(Q(customer__customer_name__icontains=field_code) | Q(order_no__icontains=field_code)).values()
            elif tbl_name == 'tblDeliveryNote_Master':
                results = model.objects.filter(Q(customer__customer_name__icontains=field_code) | Q(delivery_note_no__icontains=field_code)).values()
            elif tbl_name == 'tblQuotation_Master':
                results = model.objects.filter(Q(customer__customer_name__icontains=field_code) | Q(quotation_no__icontains=field_code)).values()
            elif tbl_name == 'tblPayment':
                results = model.objects.filter(Q(payment_no__icontains=field_code) | Q(payment_to__icontains=field_code) | Q(customer__customer_name__icontains=field_code))
            elif tbl_name == 'tblReceipt':
                results = model.objects.filter(Q(receipt_no__icontains=field_code) | Q(receipt_from__icontains=field_code) | Q(vendor__vendor_name__icontains=field_code))
        else:
            results = model.objects.all().values()
        # Create a list to store the modified data
        data = []

        # Extract the 'fields' from each entry and add the 'id' field
        for result in results:
            if tbl_name == 'tblPurchase_Master' or tbl_name == 'tblPurchaseOrder_Master' or tbl_name == 'tblPayment':
                result['vendor_name'] = tblVendor.objects.get(id=result['vendor_id']).vendor_name
            elif tbl_name == 'tblSales_Master' or tbl_name == 'tblSalesOrder_Master' or tbl_name == 'tblQuotation_Master' or tbl_name == 'tblDeliveryNotes_Master' or tbl_name == 'tblReceipt':
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


@login_required(login_url='/login')
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
    except Exception as e:
        return JsonResponse({})


@login_required(login_url='/login')
def does_field_exist(request, tbl_name, tbl_field, field_code):
    try:
        model = apps.get_model(app_label='core', model_name=tbl_name)
        if model.objects.filter(**{tbl_field: field_code}).exists():
            return JsonResponse({'result': "true"})
        else:
            return JsonResponse({})
    except:
        return JsonResponse({})