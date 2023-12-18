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
    path('company', views.companyPage, name='company'),
    path('employees', views.employeesPage, name='employees'),
    path('banking', views.bankingPage, name='banking'),
    path('reports', views.reportsPage, name='reports'),



    path('product',  views.product_view, name='product'),
    path('product/<int:frm_id>?',  views.product_view, name='product_with_id'),
    path('product_add',  views.product_add, name='product_add'),
    path('product_edit/<int:frm_id>',  views.product_edit, name='product_edit'),
    path('product_delete/<int:frm_id>',  views.product_delete, name='product_delete'),
    path('product_print/<int:frm_id>',  views.product_print, name='product_print'),
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
    path('customer_print/<int:frm_id>',  views.customer_print, name='customer_print'),
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
    path('vendor_print/<int:frm_id>',  views.vendor_print, name='vendor_print'),
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
    path('category_print/<int:frm_id>',  views.category_print, name='category_print'),
    path('category_move_first',  views.category_move_first, name='category_move_first'),
    path('category_move_previous/<int:frm_id>',  views.category_move_previous, name='category_move_previous'),
    path('category_move_next/<int:frm_id>',  views.category_move_next, name='category_move_next'),
    path('category_move_last',  views.category_move_last, name='category_move_last'),
    path('category_find',  views.category_find, name='category_find'),


    path('currency',  views.currency_view, name='currency'),
    path('currency/<int:frm_id>?',  views.currency_view, name='currency_with_id'),
    path('currency_add',  views.currency_add, name='currency_add'),
    path('currency_edit/<int:frm_id>',  views.currency_edit, name='currency_edit'),
    path('currency_delete/<int:frm_id>',  views.currency_delete, name='currency_delete'),
    path('currency_print/<int:frm_id>',  views.currency_print, name='currency_print'),
    path('currency_move_first',  views.currency_move_first, name='currency_move_first'),
    path('currency_move_previous/<int:frm_id>',  views.currency_move_previous, name='currency_move_previous'),
    path('currency_move_next/<int:frm_id>',  views.currency_move_next, name='currency_move_next'),
    path('currency_move_last',  views.currency_move_last, name='currency_move_last'),
    path('currency_find',  views.currency_find, name='currency_find'),


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
    path('save_salesOrder', views.save_salesOrder, name='save_salesOrder'),
    path('save_salesOrder/<int:order_id>', views.save_salesOrder, name='save_salesOrder'),
    path('save_purchaseOrder', views.save_purchaseOrder, name='save_purchaseOrder'),
    path('save_purchaseOrder/<int:order_id>', views.save_purchaseOrder, name='save_purchaseOrder'),
    path('save_product', views.save_product, name='save_product'),
    path('save_product/<int:product_id>', views.save_product, name='save_product'),


    # path('autocomplete', frm.autocomplete_suggestions, name='autocomplete'),
    # path('product_json', frm.product_json, name='product_json'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)