async function salesman_leave() {
    try {
        salesman = document.getElementById('master_salesman').value;
        if (salesman !== '') {
            const response = await axios.get(`/get_field_details/tblSalesman/salesman_code/salesman_name/${salesman}`)
            const data = response.data.results[0];
            if (data.id) {
                document.getElementById('master_salesman_id').value = data.id;
                document.getElementById('master_salesman').value = data.salesman_name;
            }
            else {
                document.getElementById('master_salesman_id').value = '';
                document.getElementById('master_salesman').value = '';
                toast_message(`Invalid salesman`)
            }
        }
    } catch (error) {
        document.getElementById('master_salesman_id').value = '';
        document.getElementById('master_salesman').value = '';
        toast_message(`Invalid salesman`)
        // console.error('Error fetching data:', error);
    }
}

async function customer_leave() {
    try {
        customer = document.getElementById('master_customer').value;
        if (customer !== '') {
            const response = await axios.get(`/get_field_details/tblCustomer/customer_code/customer_name/${customer}`)
            const data = response.data.results[0];
            if (data.id) {
                document.getElementById('master_customer_id').value = data.id;
                document.getElementById('master_customer').value = data.customer_name;
            }
            else {
                document.getElementById('master_customer_id').value = '';
                document.getElementById('master_customer').value = '';
                toast_message(`Invalid customer`)
            }
        }
    } catch (error) {
        document.getElementById('master_customer_id').value = '';
        document.getElementById('master_customer').value = '';
        toast_message(`Invalid customer`)
        // console.error('Error fetching data:', error);
    }
}

function salesman_keydown(event) {
    if (event.key === 'Tab' && !event.shiftKey) {
        setTimeout(() => {
            document.getElementById('tbl_product_1').focus();
        }, 0.1)
    }
}

function discount_keydown(event, index) {
    if (event.key === 'Tab' && !event.shiftKey) {
        event.preventDefault();
        var row = document.getElementById(`row${index}`);
        var qty = document.getElementById(`tbl_qty_${index}`).value;
        var tbody = row.parentNode;
        if (row === tbody.lastElementChild) {
            var newRow = document.createElement('tr');
            newRow.id = `row${index + 1}`
            newRow.innerHTML = `<td class="py-2 tbl_sl" id="tbl_sl_${index + 1}">${index + 1}</td>
            <td class="py-2 tbl_product uppercase-only" contenteditable="true" id="tbl_product_${index + 1}" onblur="product_leave(${index + 1})"></td>
            <td class="py-2 tbl_product_id" id="tbl_product_id_${index + 1}" hidden></td>
            <td class="py-2 tbl_unit">
                <select id="tbl_unit_${index + 1}">
                </select>
            </td>
            <td class="py-2 tbl_qty" oninput='totalChange(${index + 1})' contenteditable="true" id="tbl_qty_${index + 1}"></td>
            <td class="py-2 tbl_price" oninput='totalChange(${index + 1})' contenteditable="true" id="tbl_price_${index + 1}"></td>
            <td class="py-2 tbl_vat_perc" id="tbl_vat_perc_${index + 1}"></td>
            <td class="py-2 tbl_vat" id="tbl_vat_${index + 1}"></td>
            <td class="py-2 tbl_discount" oninput='totalChange(${index + 1})' onkeydown="discount_keydown(event, ${index + 1})" contenteditable="true" id="tbl_discount_${index + 1}"></td>
            <td class="py-2 tbl_total" id="tbl_total_${index + 1}"></td>`;

            tbody.appendChild(newRow);
        }
        document.getElementById(`tbl_product_${index + 1}`).focus();
    }
}

async function product_leave(index) {
    var row = document.getElementById(`row${index}`);
    var tbody = row.parentNode;
    var total_rows = tbody.childElementCount;
    var product = document.getElementById(`tbl_product_${index}`).textContent;
    if(product === '' && index === 1 && total_rows === 1) {
        console.log(index, total_rows);
        document.getElementById(`form__btn-cancel`).focus();
    }
    else if (row === tbody.lastElementChild && product === '') {
        removeRow(`row${index}`)
        document.getElementById(`form__btn-submit`).focus();
    }
    else if (product === '') {
        removeRow(`row${index}`)
        document.getElementById(`tbl_product_${index}`).focus();
    }
    else {
        try {
            const response = await axios.get(`/get_field_details/tblProduct/product_code/product_name/${product.toUpperCase()}`)
            const data = response.data.results[0];
            if (data.id) {
                document.getElementById(`tbl_product_id_${index}`).textContent = data.id;
                document.getElementById(`tbl_product_${index}`).textContent = data.product_name;
                document.getElementById(`tbl_unit_${index}`).innerHTML = '';
                var select = document.getElementById(`tbl_unit_${index}`);
                var optionElement = document.createElement("option");
                optionElement.value = data.main_unit;
                optionElement.text = data.main_unit;
                select.appendChild(optionElement);
                const units = await axios.get(`/get_field_details/tblProduct_unit/product/${data.id}`);
                units.data.results.forEach(unit => {
                    var optionElement = document.createElement("option");
                    optionElement.value = unit.unit;
                    optionElement.text = unit.unit;
                    select.appendChild(optionElement);
                })
                const vat = await axios.get(`/get_field_details/tblCategory/id/${data.category_id}`);
                document.getElementById(`tbl_vat_perc_${index}`).textContent = vat.data.results[0].vat_rate;
            }
            else {
                toast_message(`Invalid product`)
                document.getElementById(`tbl_product_id_${index}`).textContent = '';
                document.getElementById(`tbl_product_${index}`).textContent = '';
                document.getElementById(`tbl_unit_${index}`).innerHTML = '';
                document.getElementById(`tbl_vat_perc_${index}`).textContent = '';
                document.getElementById(`tbl_qty_${index}`).textContent = '';
                document.getElementById(`tbl_price_${index}`).textContent = '';
                document.getElementById(`tbl_discount_${index}`).textContent = '';
            }
        } catch (error) {
            toast_message(`Invalid product`)
            document.getElementById(`tbl_product_id_${index}`).textContent = '';
            document.getElementById(`tbl_product_${index}`).textContent = '';
            document.getElementById(`tbl_unit_${index}`).innerHTML = '';
            document.getElementById(`tbl_vat_perc_${index}`).textContent = '';
            document.getElementById(`tbl_qty_${index}`).textContent = '';
            document.getElementById(`tbl_price_${index}`).textContent = '';
            document.getElementById(`tbl_discount_${index}`).textContent = '';
        }
    }
}

function removeRow(rowId) {
    // Get the index of the row to be removed
    const rowIndex = parseInt(rowId.replace('row', ''));

    // Get the total number of rows
    const tbody = document.querySelector('tbody');
    const totalRows = tbody.querySelectorAll('tr').length;
    // Iterate over the remaining rows and update values
    for (let i = rowIndex; i < totalRows; i++) {
        const currentRow = document.getElementById(`row${i}`);
        const previousRow = document.getElementById(`row${i + 1}`);
      // Update values in the current row based on the values in the previous row
        currentRow.querySelector('.tbl_sl').innerText = i;

      // Copy values from the previous row to the current row
        currentRow.querySelector('.tbl_product').innerText = previousRow.querySelector('.tbl_product').innerText;
        currentRow.querySelector('.tbl_product_id').innerText = previousRow.querySelector('.tbl_product_id').innerText;
        currentRow.querySelector('.tbl_qty').innerText = previousRow.querySelector('.tbl_qty').innerText;
        currentRow.querySelector('.tbl_price').innerText = previousRow.querySelector('.tbl_price').innerText;
        currentRow.querySelector('.tbl_vat_perc').innerText = previousRow.querySelector('.tbl_vat_perc').innerText;
        currentRow.querySelector('.tbl_vat').innerText = previousRow.querySelector('.tbl_vat').innerText;
        currentRow.querySelector('.tbl_discount').innerText = previousRow.querySelector('.tbl_discount').innerText;
        currentRow.querySelector('.tbl_total').innerText = previousRow.querySelector('.tbl_total').innerText;
    }

    // Remove the last row
    const lastRow = document.getElementById(`row${totalRows}`);
    lastRow.remove();
}


function totalChange(index) {
    var qty = parseFloat(document.getElementById(`tbl_qty_${index}`).textContent) || 0;
    var price = parseFloat(document.getElementById(`tbl_price_${index}`).textContent) || 0;
    var discount = parseFloat(document.getElementById(`tbl_discount_${index}`).textContent) || 0;
    var vat_perc = parseFloat(document.getElementById(`tbl_vat_perc_${index}`).textContent) || 0;

    var vat = decimal_2(((qty * price) - discount) * (vat_perc/100));
    document.getElementById(`tbl_vat_${index}`).textContent = vat;

    document.getElementById(`tbl_total_${index}`).textContent = decimal_2((qty * price) + vat - discount)
    totals()
}

function totals() {
    var tbody = document.getElementById('tbl__body');
    var total_rows = tbody.childElementCount;

    var discount = 0
    var vat = 0
    var total = 0
    for (let i = 1; i <= total_rows; i++) {
        let vat_amount = parseFloat(document.getElementById(`tbl_vat_${i}`).textContent) || 0;
        let discount_amount = parseFloat(document.getElementById(`tbl_discount_${i}`).textContent) || 0;
        let total_amount = parseFloat(document.getElementById(`tbl_total_${i}`).textContent) || 0;

        vat = vat + vat_amount
        discount = discount + discount_amount
        total = total + total_amount
    }

    document.getElementById(`master_total`).value = decimal_2(total - vat + discount)
    document.getElementById(`master_vat`).value = decimal_2(vat)
    document.getElementById(`master_discount`).value = decimal_2(discount)
    netAmount()
}

function netAmount() {
    let total = parseFloat(document.getElementById(`master_total`).value) || 0;
    let vat = parseFloat(document.getElementById(`master_vat`).value) || 0;
    let discount = parseFloat(document.getElementById(`master_discount`).value) || 0;
    let roundoff = parseFloat(document.getElementById(`master_roundoff`).value) || 0;

    document.getElementById(`master_net_amount`).value = decimal_2(total + vat - discount + roundoff);
}

document.getElementById(`master_roundoff`).addEventListener('input', function() { 
    roundoff = parseFloat(document.getElementById(`master_roundoff`).value) || 0;
    if (roundoff > 1) {
        document.getElementById(`master_roundoff`).value = 1
    }
    else if (roundoff < -1) {
        document.getElementById(`master_roundoff`).value = -1
    }
    netAmount();
})



function save_quotation(event, id) {
    event.preventDefault();

    if (is_field_empty('#master_customer_id', 'Please enter a valid customer')) {
        return;
    } else if ($('#tbl_product_1').text() === null || $('#tbl_product_1').text() === '') {
        toast_message('no products added')
        $('#tbl_product_1').focus();
        return;
    }

    var quotation_no = document.getElementById(`master_quotation_no`).value;
    var quotation_date = document.getElementById(`master_quotation_date`).value;
    var total = document.getElementById('master_total').value;
    var discount = document.getElementById('master_discount').value;
    var vat = document.getElementById('master_vat').value;
    var roundoff = document.getElementById('master_roundoff').value;
    var net_amount = document.getElementById('master_net_amount').value;
    var customer = document.getElementById('master_customer_id').value;
    var salesman = document.getElementById('master_salesman_id').value;

    var master_data = [];
    master_data.push(quotation_no, quotation_date, total, discount, vat, roundoff, net_amount, customer, salesman);

    var url_link = id? `/save_quotation/` + id : `/save_quotation`;
    save_details(master_data, url_link)
}

async function save_details(master_data, url_link) {
    var tbl = document.getElementById('tbl__body');
    var row_count = tbl.childElementCount;
    var details_data = [];
    for (let i = 1; i <= row_count; i++) {
        var product = document.getElementById(`tbl_product_id_${i}`).textContent;
        var unit = document.getElementById(`tbl_unit_${i}`).value;
        var qty = document.getElementById(`tbl_qty_${i}`).textContent;
        var price = document.getElementById(`tbl_price_${i}`).textContent;
        var vat_perc = document.getElementById(`tbl_vat_perc_${i}`).textContent;
        var vat = document.getElementById(`tbl_vat_${i}`).textContent;
        var discount = document.getElementById(`tbl_discount_${i}`).textContent;
        var total = document.getElementById(`tbl_total_${i}`).textContent;
        details_data.push([product, unit, qty, price, vat_perc, vat, discount, total]);
    }
    try {    
        var data = {
            master_data: master_data,
            details_data: details_data
        };
        var header = {headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // You need a function to get the CSRF token
        }}
        var result = await axios.post(url_link, JSON.stringify(data), header)
        document.getElementById('form__btn-submit').closest('form').submit();
    }
    catch (e) {

    }
}


function formSearch() {
    row = document.getElementById("tbl__body");
    row.innerHTML = '';
    search_val = document.getElementById('formSearch').value;
    if (search_val === '' || search_val === undefined) {
        findRow(`form_search/tblQuotation_Master`, row);
        return;
    }
    search_in = document.getElementById('cmbFormSearch').value;
    switch(search_in) {
        case `quotation_no`:
            findRow(`form_search/tblQuotation_Master/quotation_no/` + search_val, row);
            break;
        case 'customer_name':
            findRow(`form_search/tblQuotation_Master/customer__customer_name/` + search_val, row);
            break;
        case `quotation_date`:
            findRow(`form_search/tblQuotation_Master/quotation_date/` + search_val, row);
            break;
        default:
            findRow(`form_search/tblQuotation_Master/` + search_val, row);
    }
}

async function findRow(url_link, row) {
    try {
        rowCounter = 1;
        var response = await axios.get(url_link)
        response.data.forEach(item => {
            new_row = `<tr class="form-list__contents">` +
                `<td class="py-2"><p class="text-black font-semibold text-base">${rowCounter}</p></td>` +
                `<td class="py-2"><a href="/quotation/${item.id}"><p class="text-black font-semibold text-base">${item.quotation_no}</p></a></td>` +
                `<td class="py-2"><p class="text-black font-semibold text-base">${item.quotation_date}</p></td>` +
                `<td class="py-2"><a href="/quotation/${item.id}"><p class="text-black font-semibold text-base">${item.customer_name}</p></a></td>` +
                `<td class="py-2"><p class="text-black font-semibold text-base">${item.net_amount}</p></td>` +
                `</tr>`;

            row.innerHTML = new_row;
            rowCounter++;
        })
    }
    catch(error) {
        console.error('Error in Axios request:', error);
    }
}