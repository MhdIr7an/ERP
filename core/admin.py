from django.contrib import admin

from . models import (tblUsers, tblCategory, tblProduct, tblProduct_unit, tblCustomer, tblVendor, tblPurchase_Master, tblPurchase_Details, tblSales_Master, tblSales_Details, tblSalesman,
                    tblReceipt, tblPayment, tblDeliveryNote_Master, tblDeliveryNote_Details, tblPurchaseOrder_Master, tblPurchaseOrder_Details, tblSalesOrder_Master, tblSalesOrder_Details,
                    tblQuotation_Master, tblQuotation_Details)

admin.site.register(tblUsers)
admin.site.register(tblCategory)
admin.site.register(tblProduct)
admin.site.register(tblProduct_unit)
admin.site.register(tblCustomer)
admin.site.register(tblVendor)
admin.site.register(tblSalesman)
admin.site.register(tblPurchase_Master)
admin.site.register(tblPurchase_Details)
admin.site.register(tblSales_Master)
admin.site.register(tblSales_Details)
admin.site.register(tblReceipt)
admin.site.register(tblPayment)
admin.site.register(tblDeliveryNote_Master)
admin.site.register(tblDeliveryNote_Details)
admin.site.register(tblPurchaseOrder_Master)
admin.site.register(tblPurchaseOrder_Details)
admin.site.register(tblSalesOrder_Master)
admin.site.register(tblSalesOrder_Details)
admin.site.register(tblQuotation_Master)
admin.site.register(tblQuotation_Details)