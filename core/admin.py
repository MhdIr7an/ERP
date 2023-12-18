from django.contrib import admin

from . models import tblUsers, tblCategory, tblProduct, tblProduct_unit, tblCustomer, tblVendor, tblPurchase_Master, tblPurchase_Details, tblSales_Master, tblSales_Details

admin.site.register(tblUsers)
admin.site.register(tblCategory)
admin.site.register(tblProduct)
admin.site.register(tblProduct_unit)
admin.site.register(tblCustomer)
admin.site.register(tblVendor)
admin.site.register(tblPurchase_Master)
admin.site.register(tblPurchase_Details)
admin.site.register(tblSales_Master)
admin.site.register(tblSales_Details)