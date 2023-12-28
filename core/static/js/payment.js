var credit = parseFloat(document.getElementById('credit_balance').value) || 0;
var amount = parseFloat(document.getElementById('amount').value) || 0;
var discount = parseFloat(document.getElementById('discount').value) || 0;
var credit_balance = credit + amount + discount;

async function vendor_leave() {
    try {
        vendor = document.getElementById('vendor').value;
        if (vendor !== '') {
            const response = await axios.get(`/get_field_details/tblVendor/vendor_code/vendor_name/${vendor}`)
            const data = response.data.results[0];
            if (data.id) {
                document.getElementById('vendor_id').value = data.id;
                document.getElementById('vendor').value = data.vendor_name;
                document.getElementById('credit_balance').value = data.credit_balance;
                credit_balance = data.credit_balance;
                creditChange();
            }
            else {
                document.getElementById('vendor_id').value = '';
                document.getElementById('vendor').value = '';
                document.getElementById('credit_balance').value = '';
                toast_message(`Invalid vendor`)
                creditChange = 0;
                creditChange();
            }
        }
    } catch (error) {
        document.getElementById('vendor_id').value = '';
        document.getElementById('vendor').value = '';
        document.getElementById('credit_balance').value = '';
        toast_message(`Invalid vendor`)
        creditChange = 0;
        creditChange();
        // console.error('Error fetching data:', error);
    }
}

async function customer_leave() {
    try {
        customer = document.getElementById('customer').value;
        if (customer !== '') {
            const response = await axios.get(`/get_field_details/tblCustomer/customer_code/customer_name/${customer}`)
            const data = response.data.results[0];
            if (data.id) {
                document.getElementById('customer_id').value = data.id;
                document.getElementById('customer').value = data.customer_name;
                document.getElementById('credit_balance').value = data.credit_balance;
                credit_balance = data.credit_balance;
                creditChange();
            }
            else {
                document.getElementById('customer_id').value = '';
                document.getElementById('customer').value = '';
                document.getElementById('credit_balance').value = '';
                toast_message(`Invalid customer`)
                creditChange = 0;
                creditChange();
            }
        }
    } catch (error) {
        document.getElementById('customer_id').value = '';
        document.getElementById('customer').value = '';
        document.getElementById('credit_balance').value = '';
        toast_message(`Invalid customer`)
        creditChange = 0;
        creditChange();
        // console.error('Error fetching data:', error);
    }
}

async function savePaymentOrReceipt(event, paymentOrReceipt, id) {
    event.preventDefault();

    // if (((paymentOrReceipt === 'payment')?is_field_empty('#vendor_id', 'Please enter a valid vendor'):is_field_empty('#customer_id', 'Please enter a valid customer'))) {
        //     return;
        // }
    
    if (paymentOrReceipt === 'payment') {
        var payment_no = document.getElementById('payment_no').value;
        var payment_date = document.getElementById('payment_date').value;
        var vendor_to = document.getElementById('vendor_to').value;
        var vendor = (vendor_to === 1)? document.getElementById('vendor_id').value : '';
        var payment_to = (vendor_to === 1)? '' : document.getElementById('payment_to').value;
        var discount = (vendor_to === 1)? document.getElementById('discount').value : 0;
    }
    else {
        var receipt_no = document.getElementById('receipt_no').value;
        var receipt_date = document.getElementById('receipt_date').value;
        var customer_from = document.getElementById('customer_from').value;
        var customer = (customer_from === 1)? document.getElementById('customer_id').value : '';
        var receipt_from = (customer_from === 1)? '' : document.getElementById('receipt_from').value;
        var discount = (customer_from === 1)? document.getElementById('discount').value : 0;
    }

    var amount = document.getElementById('amount').value;
    var payment_method = document.getElementById('payment_method').value;

    var data = [];
    data.push((paymentOrReceipt === 'payment')?payment_no:receipt_no, (paymentOrReceipt === 'payment')?payment_date:receipt_date, (paymentOrReceipt === 'payment')?vendor:customer, (paymentOrReceipt === 'payment')?payment_to:receipt_from, amount, discount, payment_method);

    var url_link = id? `/save_${(paymentOrReceipt === 'payment')?`payment`:`receipt`}/` + id : `/save_${(paymentOrReceipt === 'payment')?`payment`:`receipt`}`;
    var header = {headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
    }}
    await axios.post(url_link, JSON.stringify(data), header)
    document.getElementById('form__btn-submit').closest('form').submit();
}

document.getElementById('amount').addEventListener('input', function() {
    creditChange();
})

document.getElementById('discount').addEventListener('input', function() {
    creditChange();
})

function creditChange() {
    var amount = parseFloat(document.getElementById('amount').value) || 0;
    var discount = parseFloat(document.getElementById('discount').value) || 0;

    total = credit_balance - amount - discount;
    document.getElementById('credit_balance').value = total
}

function formSearch(paymentOrReceipt) {
    row = $("#tbl__body");
    rowCounter = 1;
    row.html('');
    search_val = $('#formSearch').val();
    if (search_val === '' || search_val === undefined) {
        findRow(`form_search/tbl${paymentOrReceipt}`, row, paymentOrReceipt);
        return;
    }
    search_in = $('#cmbFormSearch').val();
    switch(search_in) {
        case 'receipt_no':
            findRow(`form_search/tblReceipt/receipt_no/` + search_val, row, paymentOrReceipt);
            break;
        case 'receipt_date':
            findRow(`form_search/tblReceipt/receipt_date/` + search_val, row, paymentOrReceipt);
            break;
        case 'receipt_from':
            findRow(`form_search/tblReceipt/receipt_from/customer__customer_name/` + search_val, row, paymentOrReceipt);
            break;
        case 'payment_no':
            findRow(`form_search/tblPayment/payment_no/` + search_val, row, paymentOrReceipt);
            break;
        case 'payment_date':
            findRow(`form_search/tblPayment/payment_date/` + search_val, row, paymentOrReceipt);
            break;
        case 'payment_to':
            findRow(`form_search/tblPayment/payment_to/vendor__vendor_name` + search_val, row, paymentOrReceipt);
            break;
        default:
            findRow(`form_search/tbl${paymentOrReceipt}/` + search_val, row, paymentOrReceipt);
    }

}


function findRow(url_link, row) {
    rowCounter = 1;
    axios.get(url_link)
    .then(response => {
        response.data.forEach(item => {
            new_row = `<tr class="form-list__contents">` +
                `<td class="py-2"><p class="text-black font-semibold text-base">` + rowCounter + `</p></td>` +
                `<td class="py-2"><a href="/${(paymentOrReceipt === 'Payment')?'payment':'receipt'}/` + item.id + `"><p class="text-black font-semibold text-base">` + (paymentOrReceipt === `Payment`)?item.payment_no:item.receipt_no + `</p></a></td>` +
                `<td class="py-2"><p class="text-black font-semibold text-base">` + (paymentOrReceipt === `Payment`)?item.payment_date:item.receipt_date + `</p></td>` +
                `<td class="py-2"><p class="text-black font-semibold text-base">` + (paymentOrReceipt === `Payment`)?((item.payment_to)?item.payment_to:item.vendor_name):((item.receipt_from)?item.receipt_from:item.customer_name) + `</p></a></td>` +
                `<td class="py-2"><p class="text-black font-semibold text-base">` + item.amount + `</p></td>` +
                `<td class="py-2"><p class="text-black font-semibold text-base">` + item.discount + `</p></td>` +
                `</tr>`;

            row.append(new_row);
            rowCounter++;
        })
    })
    .catch(error => {
        console.error('Error in Axios request:', error);
    });
}

function vendor_toChange() {
    var vendor_to = document.getElementById('vendor_to')
    var vendor = document.querySelector('.vendor-field');
    var to = document.querySelector('.to-field');
    var discount = document.getElementById('discount-grp');
    var credit_balance = document.getElementById('credit_balance-grp');
    if (vendor.style.display == 'none') {
        vendor.style.display = 'block';
        to.style.display = 'none';
        discount.style.display = 'block';
        credit_balance.style.display = 'block';
        vendor_to.value = 1;
    }
    else {
        vendor.style.display = 'none';
        to.style.display = 'block';
        discount.style.display = 'none';
        credit_balance.style.display = 'none';
        vendor_to.value = 0;
    }
}

function customer_fromChange() {
    var customer_from = document.getElementById('customer_from')
    var customer = document.querySelector('.customer-field');
    var from = document.querySelector('.from-field');
    var discount = document.getElementById('discount-grp');
    var credit_balance = document.getElementById('credit_balance-grp');
    if (customer.style.display == 'none') {
        customer.style.display = 'block';
        from.style.display = 'none';
        discount.style.display = 'block';
        credit_balance.style.display = 'block';
        customer_from.value = 1;
    }
    else {
        customer.style.display = 'none';
        from.style.display = 'block';
        discount.style.display = 'none';
        credit_balance.style.display = 'none';
        customer_from.value = 0;
    }
}