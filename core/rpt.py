from django.http import HttpResponse

from django.template.loader import get_template
import pdfkit
from .models import (tblPurchase_Master, tblPurchase_Details, tblSales_Master, tblSales_Details, tblPurchaseOrder_Master, tblPurchaseOrder_Details, tblSalesOrder_Master, tblSalesOrder_Details,
                    tblQuotation_Master, tblQuotation_Details, tblDeliveryNote_Master, tblDeliveryNote_Details)
from .convertions import to_decimal, to_integer
from num2words import num2words

def invoice_print(request, id, module_name):
    # Get your HTML template
    templates = {
        'sales': 'reports/invoice.html',
        'purchase': 'reports/invoice.html',
        'salesReturn': 'reports/return.html',
        'purchaseReturn': 'reports/return.html',
        'salesOrder': 'reports/order.html',
        'purchaseOrder': 'reports/order.html',
        'quotation': 'reports/quotation.html',
        'deliveryNote': 'reports/deliveryNote.html',
    }
    if module_name in templates:
        template = get_template(templates[module_name])
    
    if module_name == 'purchase':
        # Context data for rendering the template
        master = tblPurchase_Master.objects.get(id = id, transaction_type = '')
        details = tblPurchase_Details.objects.filter(purchase = master)
    elif module_name == 'sales':
        master = tblSales_Master.objects.get(id = id, transaction_type = '')
        details = tblSales_Details.objects.filter(sales = master)
    elif module_name == 'purchaseReturn':
        # Context data for rendering the template
        master = tblPurchase_Master.objects.get(id = id, transaction_type = 'return')
        details = tblPurchase_Details.objects.filter(purchase = master)
    elif module_name == 'salesReturn':
        master = tblSales_Master.objects.get(id = id, transaction_type = 'return')
        details = tblSales_Details.objects.filter(sales = master)
    elif module_name == 'purchaseOrder':
        # Context data for rendering the template
        master = tblPurchaseOrder_Master.objects.get(id = id)
        details = tblPurchaseOrder_Details.objects.filter(purchase_order = master)
    elif module_name == 'salesOrder':
        master = tblSalesOrder_Master.objects.get(id = id)
        details = tblSalesOrder_Details.objects.filter(sales_order = master)
    elif module_name == 'quotation':
        master = tblQuotation_Master.objects.get(id = id)
        details = tblQuotation_Details.objects.filter(quotation = master)
    elif module_name == 'deliveryNote':
        master = tblDeliveryNote_Master.objects.get(id = id)
        details = tblDeliveryNote_Details.objects.filter(delivery_note = master)

    total_amt = 0
    for detail in details:
        total_amt = total_amt + to_decimal(detail.total_amount)
    total = str(master.net_amount).split('.')
    total_in_words = num2words(total[0])
    if to_integer(total[1]) > 0:
        total_in_words = total_in_words + ' and ' + num2words(total[1])
    context = {'module_name': module_name, 'master': master, 'details': details, 'total_amt': total_amt, 'total_in_words': total_in_words.title()}

    # Render the template with the context data
    html_content = template.render(context)

    # Generate PDF using pdfkit
    pdf_file = pdfkit.from_string(html_content, False, configuration=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'))

    # Create an HTTP response with PDF content
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'

    return response
