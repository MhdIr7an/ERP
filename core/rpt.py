from django.http import HttpResponse

# import PyPDF2

from .models import tblCustomer

from django.template.loader import get_template
import pdfkit
from .models import tblPurchase_Master, tblPurchase_Details, tblSales_Master, tblSales_Details
from django.conf import settings
from .convertions import to_decimal, to_integer
from num2words import num2words

def invoice_print(request, id, module_name):
    # Get your HTML template
    template = get_template('reports/invoice.html')
    
    if module_name == 'purchase':
        # Context data for rendering the template
        master = tblPurchase_Master.objects.get(id = id)
        details = tblPurchase_Details.objects.filter(purchase = master)
    elif module_name == 'sales':
        master = tblSales_Master.objects.get(id = id)
        details = tblSales_Details.objects.filter(sales = master)

    total_amt = 0
    for detail in details:
        total_amt = total_amt + to_decimal(detail.total_amount)
    total = str(master.net_amount).split('.')
    total_in_words = num2words(total[0]) + ' AED'
    if to_integer(total[1]) > 0:
        total_in_words = total_in_words + ' and ' + num2words(total[1]) + ' F'
    context = {'module_name': module_name, 'master': master, 'details': details, 'total_amt': total_amt, 'total_in_words': total_in_words.title()}

    # Render the template with the context data
    html_content = template.render(context)

    # Generate PDF using pdfkit
    pdf_file = pdfkit.from_string(html_content, False, configuration=pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_BIN_PATH))

    # Create an HTTP response with PDF content
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'

    return response
