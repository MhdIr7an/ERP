from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginPage, name='login'),
    path('register', views.registerPage, name='register'),
    path('logout', views.logoutUser, name='logout'),
    path('home', views.homePage, name='home'),



    path('product',  views.product_view, name='product'),
    path('product/<int:frm_id>?',  views.product_view, name='product_with_id'),
    path('product_add',  views.product_add, name='product_add'),
    path('product_edit/<int:frm_id>',  views.product_edit, name='product_edit'),
    path('product_delete/<int:frm_id>',  views.product_delete, name='product_delete'),
    path('product_move_first',  views.product_move_first, name='product_move_first'),
    path('product_move_previous/<int:frm_id>',  views.product_move_previous, name='product_move_previous'),
    path('product_move_next/<int:frm_id>',  views.product_move_next, name='product_move_next'),
    path('product_move_last',  views.product_move_last, name='product_move_last'),
    path('product_find',  views.product_find, name='product_find'),



    path('customer',  views.customer_view, name='customer'),
    path('customer/<int:frm_id>?',  views.customer_view, name='customer_with_id'),
    path('customer_add',  views.customer_add, name='customer_add'),
    path('customer_edit/<int:frm_id>',  views.customer_edit, name='customer_edit'),
    path('customer_delete/<int:frm_id>',  views.customer_delete, name='customer_delete'),
    path('customer_move_first',  views.customer_move_first, name='customer_move_first'),
    path('customer_move_previous/<int:frm_id>',  views.customer_move_previous, name='customer_move_previous'),
    path('customer_move_next/<int:frm_id>',  views.customer_move_next, name='customer_move_next'),
    path('customer_move_last',  views.customer_move_last, name='customer_move_last'),
    path('customer_find',  views.customer_find, name='customer_find'),



    path('vendor',  views.vendor_view, name='vendor'),
    path('vendor/<int:frm_id>?',  views.vendor_view, name='vendor_with_id'),
    path('vendor_add',  views.vendor_add, name='vendor_add'),
    path('vendor_edit/<int:frm_id>',  views.vendor_edit, name='vendor_edit'),
    path('vendor_delete/<int:frm_id>',  views.vendor_delete, name='vendor_delete'),
    path('vendor_move_first',  views.vendor_move_first, name='vendor_move_first'),
    path('vendor_move_previous/<int:frm_id>',  views.vendor_move_previous, name='vendor_move_previous'),
    path('vendor_move_next/<int:frm_id>',  views.vendor_move_next, name='vendor_move_next'),
    path('vendor_move_last',  views.vendor_move_last, name='vendor_move_last'),
    path('vendor_find',  views.vendor_find, name='vendor_find'),


    path('category',  views.category_view, name='category'),
    path('category/<int:frm_id>?',  views.category_view, name='category_with_id'),
    path('category_add',  views.category_add, name='category_add'),
    path('category_edit/<int:frm_id>',  views.category_edit, name='category_edit'),
    path('category_delete/<int:frm_id>',  views.category_delete, name='category_delete'),
    path('category_move_first',  views.category_move_first, name='category_move_first'),
    path('category_move_previous/<int:frm_id>',  views.category_move_previous, name='category_move_previous'),
    path('category_move_next/<int:frm_id>',  views.category_move_next, name='category_move_next'),
    path('category_move_last',  views.category_move_last, name='category_move_last'),
    path('category_find',  views.category_find, name='category_find'),


    path('salesman',  views.salesman_view, name='salesman'),
    path('salesman/<int:frm_id>',  views.salesman_view, name='salesman_with_id'),
    path('salesman_add',  views.salesman_add, name='salesman_add'),
    path('salesman_edit/<int:frm_id>',  views.salesman_edit, name='salesman_edit'),
    path('salesman_delete/<int:frm_id>',  views.salesman_delete, name='salesman_delete'),
    path('salesman_move_first',  views.salesman_move_first, name='salesman_move_first'),
    path('salesman_move_previous/<int:frm_id>',  views.salesman_move_previous, name='salesman_move_previous'),
    path('salesman_move_next/<int:frm_id>',  views.salesman_move_next, name='salesman_move_next'),
    path('salesman_move_last',  views.salesman_move_last, name='salesman_move_last'),
    path('salesman_find',  views.salesman_find, name='salesman_find'),


    path('sales',  views.sales_view, name='sales'),
    path('sales/<int:frm_id>',  views.sales_view, name='sales_with_id'),
    path('sales_add',  views.sales_add, name='sales_add'),
    path('sales_edit/<int:frm_id>',  views.sales_edit, name='sales_edit'),
    path('sales_delete/<int:frm_id>',  views.sales_delete, name='sales_delete'),
    path('sales_print/<int:frm_id>',  views.sales_print, name='sales_print'),
    path('sales_move_first',  views.sales_move_first, name='sales_move_first'),
    path('sales_move_previous/<int:frm_id>',  views.sales_move_previous, name='sales_move_previous'),
    path('sales_move_next/<int:frm_id>',  views.sales_move_next, name='sales_move_next'),
    path('sales_move_last',  views.sales_move_last, name='sales_move_last'),
    path('sales_find',  views.sales_find, name='sales_find'),



    path('purchase',  views.purchase_view, name='purchase'),
    path('purchase/<int:frm_id>',  views.purchase_view, name='purchase_with_id'),
    path('purchase_add',  views.purchase_add, name='purchase_add'),
    path('purchase_edit/<int:frm_id>',  views.purchase_edit, name='purchase_edit'),
    path('purchase_delete/<int:frm_id>',  views.purchase_delete, name='purchase_delete'),
    path('purchase_print/<int:frm_id>',  views.purchase_print, name='purchase_print'),
    path('purchase_move_first',  views.purchase_move_first, name='purchase_move_first'),
    path('purchase_move_previous/<int:frm_id>',  views.purchase_move_previous, name='purchase_move_previous'),
    path('purchase_move_next/<int:frm_id>',  views.purchase_move_next, name='purchase_move_next'),
    path('purchase_move_last',  views.purchase_move_last, name='purchase_move_last'),
    path('purchase_find',  views.purchase_find, name='purchase_find'),




    path('salesReturn',  views.salesReturn_view, name='salesReturn'),
    path('salesReturn/<int:frm_id>',  views.salesReturn_view, name='salesReturn_with_id'),
    path('salesReturn_add',  views.salesReturn_add, name='salesReturn_add'),
    path('salesReturn_edit/<int:frm_id>',  views.salesReturn_edit, name='salesReturn_edit'),
    path('salesReturn_delete/<int:frm_id>',  views.salesReturn_delete, name='salesReturn_delete'),
    path('salesReturn_print/<int:frm_id>',  views.salesReturn_print, name='salesReturn_print'),
    path('salesReturn_move_first',  views.salesReturn_move_first, name='salesReturn_move_first'),
    path('salesReturn_move_previous/<int:frm_id>',  views.salesReturn_move_previous, name='salesReturn_move_previous'),
    path('salesReturn_move_next/<int:frm_id>',  views.salesReturn_move_next, name='salesReturn_move_next'),
    path('salesReturn_move_last',  views.salesReturn_move_last, name='salesReturn_move_last'),
    path('salesReturn_find',  views.salesReturn_find, name='salesReturn_find'),



    path('purchaseReturn',  views.purchaseReturn_view, name='purchaseReturn'),
    path('purchaseReturn/<int:frm_id>',  views.purchaseReturn_view, name='purchaseReturn_with_id'),
    path('purchaseReturn_add',  views.purchaseReturn_add, name='purchaseReturn_add'),
    path('purchaseReturn_edit/<int:frm_id>',  views.purchaseReturn_edit, name='purchaseReturn_edit'),
    path('purchaseReturn_delete/<int:frm_id>',  views.purchaseReturn_delete, name='purchaseReturn_delete'),
    path('purchaseReturn_print/<int:frm_id>',  views.purchaseReturn_print, name='purchaseReturn_print'),
    path('purchaseReturn_move_first',  views.purchaseReturn_move_first, name='purchaseReturn_move_first'),
    path('purchaseReturn_move_previous/<int:frm_id>',  views.purchaseReturn_move_previous, name='purchaseReturn_move_previous'),
    path('purchaseReturn_move_next/<int:frm_id>',  views.purchaseReturn_move_next, name='purchaseReturn_move_next'),
    path('purchaseReturn_move_last',  views.purchaseReturn_move_last, name='purchaseReturn_move_last'),
    path('purchaseReturn_find',  views.purchaseReturn_find, name='purchaseReturn_find'),



    path('purchaseOrder',  views.purchaseOrder_view, name='purchaseOrder'),
    path('purchaseOrder/<int:frm_id>',  views.purchaseOrder_view, name='purchaseOrder_with_id'),
    path('purchaseOrder_add',  views.purchaseOrder_add, name='purchaseOrder_add'),
    path('purchaseOrder_edit/<int:frm_id>',  views.purchaseOrder_edit, name='purchaseOrder_edit'),
    path('purchaseOrder_delete/<int:frm_id>',  views.purchaseOrder_delete, name='purchaseOrder_delete'),
    path('purchaseOrder_print/<int:frm_id>',  views.purchaseOrder_print, name='purchaseOrder_print'),
    path('purchaseOrder_move_first',  views.purchaseOrder_move_first, name='purchaseOrder_move_first'),
    path('purchaseOrder_move_previous/<int:frm_id>',  views.purchaseOrder_move_previous, name='purchaseOrder_move_previous'),
    path('purchaseOrder_move_next/<int:frm_id>',  views.purchaseOrder_move_next, name='purchaseOrder_move_next'),
    path('purchaseOrder_move_last',  views.purchaseOrder_move_last, name='purchaseOrder_move_last'),
    path('purchaseOrder_find',  views.purchaseOrder_find, name='purchaseOrder_find'),



    path('salesOrder',  views.salesOrder_view, name='salesOrder'),
    path('salesOrder/<int:frm_id>',  views.salesOrder_view, name='salesOrder_with_id'),
    path('salesOrder_add',  views.salesOrder_add, name='salesOrder_add'),
    path('salesOrder_edit/<int:frm_id>',  views.salesOrder_edit, name='salesOrder_edit'),
    path('salesOrder_delete/<int:frm_id>',  views.salesOrder_delete, name='salesOrder_delete'),
    path('salesOrder_print/<int:frm_id>',  views.salesOrder_print, name='salesOrder_print'),
    path('salesOrder_move_first',  views.salesOrder_move_first, name='salesOrder_move_first'),
    path('salesOrder_move_previous/<int:frm_id>',  views.salesOrder_move_previous, name='salesOrder_move_previous'),
    path('salesOrder_move_next/<int:frm_id>',  views.salesOrder_move_next, name='salesOrder_move_next'),
    path('salesOrder_move_last',  views.salesOrder_move_last, name='salesOrder_move_last'),
    path('salesOrder_find',  views.salesOrder_find, name='salesOrder_find'),



    path('quotation',  views.quotation_view, name='quotation'),
    path('quotation/<int:frm_id>',  views.quotation_view, name='quotation_with_id'),
    path('quotation_add',  views.quotation_add, name='quotation_add'),
    path('quotation_edit/<int:frm_id>',  views.quotation_edit, name='quotation_edit'),
    path('quotation_delete/<int:frm_id>',  views.quotation_delete, name='quotation_delete'),
    path('quotation_print/<int:frm_id>',  views.quotation_print, name='quotation_print'),
    path('quotation_move_first',  views.quotation_move_first, name='quotation_move_first'),
    path('quotation_move_previous/<int:frm_id>',  views.quotation_move_previous, name='quotation_move_previous'),
    path('quotation_move_next/<int:frm_id>',  views.quotation_move_next, name='quotation_move_next'),
    path('quotation_move_last',  views.quotation_move_last, name='quotation_move_last'),
    path('quotation_find',  views.quotation_find, name='quotation_find'),



    path('deliveryNote',  views.deliveryNote_view, name='deliveryNote'),
    path('deliveryNote/<int:frm_id>',  views.deliveryNote_view, name='deliveryNote_with_id'),
    path('deliveryNote_add',  views.deliveryNote_add, name='deliveryNote_add'),
    path('deliveryNote_edit/<int:frm_id>',  views.deliveryNote_edit, name='deliveryNote_edit'),
    path('deliveryNote_delete/<int:frm_id>',  views.deliveryNote_delete, name='deliveryNote_delete'),
    path('deliveryNote_print/<int:frm_id>',  views.deliveryNote_print, name='deliveryNote_print'),
    path('deliveryNote_move_first',  views.deliveryNote_move_first, name='deliveryNote_move_first'),
    path('deliveryNote_move_previous/<int:frm_id>',  views.deliveryNote_move_previous, name='deliveryNote_move_previous'),
    path('deliveryNote_move_next/<int:frm_id>',  views.deliveryNote_move_next, name='deliveryNote_move_next'),
    path('deliveryNote_move_last',  views.deliveryNote_move_last, name='deliveryNote_move_last'),
    path('deliveryNote_find',  views.deliveryNote_find, name='deliveryNote_find'),



    path('payment',  views.payment_view, name='payment'),
    path('payment/<int:frm_id>',  views.payment_view, name='payment_with_id'),
    path('payment_add',  views.payment_add, name='payment_add'),
    path('payment_edit/<int:frm_id>',  views.payment_edit, name='payment_edit'),
    path('payment_delete/<int:frm_id>',  views.payment_delete, name='payment_delete'),
    path('payment_move_first',  views.payment_move_first, name='payment_move_first'),
    path('payment_move_previous/<int:frm_id>',  views.payment_move_previous, name='payment_move_previous'),
    path('payment_move_next/<int:frm_id>',  views.payment_move_next, name='payment_move_next'),
    path('payment_move_last',  views.payment_move_last, name='payment_move_last'),
    path('payment_find',  views.payment_find, name='payment_find'),



    path('receipt',  views.receipt_view, name='receipt'),
    path('receipt/<int:frm_id>',  views.receipt_view, name='receipt_with_id'),
    path('receipt_add',  views.receipt_add, name='receipt_add'),
    path('receipt_edit/<int:frm_id>',  views.receipt_edit, name='receipt_edit'),
    path('receipt_delete/<int:frm_id>',  views.receipt_delete, name='receipt_delete'),
    path('receipt_move_first',  views.receipt_move_first, name='receipt_move_first'),
    path('receipt_move_previous/<int:frm_id>',  views.receipt_move_previous, name='receipt_move_previous'),
    path('receipt_move_next/<int:frm_id>',  views.receipt_move_next, name='receipt_move_next'),
    path('receipt_move_last',  views.receipt_move_last, name='receipt_move_last'),
    path('receipt_find',  views.receipt_find, name='receipt_find'),



    path('get_field_details/<str:tbl_name>/<str:tbl_field>/<str:field_code>', views.get_field_details, name='get_field_details'),
    path('get_field_details/<str:tbl_name>/<str:tbl_field>/<str:tbl_field_2>/<str:field_code>', views.get_field_details, name='get_field_details'),
    path('does_field_exist/<str:tbl_name>/<str:tbl_field>/<str:field_code>', views.does_field_exist, name='does_field_exist'),
    
    path('form_search/<str:tbl_name>/', views.formSearch, name='form_search'),
    path('form_search/<str:tbl_name>/<str:field_code>', views.formSearch, name='form_search'),
    path('form_search/<str:tbl_name>/<str:tbl_field>/<str:field_code>', views.formSearch, name='form_search'),
    path('form_search/<str:tbl_name>/<str:tbl_field>/<str:tbl_field_2>/<str:field_code>', views.formSearch, name='form_search'),




    path('save_sales', views.save_sales, name='save_sales'),
    path('save_sales/<int:sales_id>', views.save_sales, name='save_sales'),
    path('save_purchase', views.save_purchase, name='save_purchase'),
    path('save_purchase/<int:purchase_id>', views.save_purchase, name='save_purchase'),
    path('save_product', views.save_product, name='save_product'),
    path('save_product/<int:product_id>', views.save_product, name='save_product'),
    path('save_purchaseOrder', views.save_purchaseOrder, name='save_purchaseOrder'),
    path('save_purchaseOrder/<int:order_id>', views.save_purchaseOrder, name='save_purchaseOrder'),
    path('save_salesOrder', views.save_salesOrder, name='save_salesOrder'),
    path('save_salesOrder/<int:order_id>', views.save_salesOrder, name='save_salesOrder'),
    path('save_quotation', views.save_quotation, name='save_quotation'),
    path('save_quotation/<int:quotation_id>', views.save_quotation, name='save_quotation'),
    path('save_deliveryNote', views.save_deliveryNote, name='save_deliveryNote'),
    path('save_deliveryNote/<int:deliveryNote_id>', views.save_deliveryNote, name='save_deliveryNote'),
    path('save_payment', views.save_payment, name='save_payment'),
    path('save_payment/<int:payment_id>', views.save_payment, name='save_payment'),
    path('save_receipt', views.save_receipt, name='save_receipt'),
    path('save_receipt/<int:receipt_id>', views.save_receipt, name='save_receipt'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)