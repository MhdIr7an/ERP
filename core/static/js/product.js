function saveProduct(event, product_id) {
    event.preventDefault();

    if (is_field_empty('#product_code', 'Enter Product Code')) {
        return;
    } else if (is_field_empty('#product_main_unit', 'Select a Product Unit')) {
        return;
    } else if (is_field_empty('#product_product_name', 'Enter Product Name')) {
        return;
    } else if (is_field_empty('#product_stock', 'Enter Stock')) {
        return;
    } else if (is_field_empty('#product_cost_price', 'Enter Cost price')) {
        return;
    } else if (is_field_empty('#product_selling_price', 'Enter Selling Price')) {
        return;
    } else if (is_field_empty('#product_vendor', 'Enter Vendor')) {
        return;
    } else if (is_field_empty('#product_category', 'Enter Category')) {
        return;
    } else if ($('#product_vendor').val() === 'Enter a valid vendor code/name') {
        alert('Please enter a valid vendor code');
        $('#product_vendor').focus();
        return;
    } else if ($('#product_category').val() === 'Enter a valid category code/name') {
        alert('Please enter a valid category code');
        $('#product_category').focus();
        return;
    } else {
        // Create an array to store the field values
        var product_data = [];
            
        // Retrieve and store the values of each field
        product_data.push($('#product_code').val());
        product_data.push($('#product_name').val());
        // product_data.push(date_to_yyyymmdd('#master_invoice_date'));
        product_data.push($('#product_main_unit').val());
        product_data.push($('#product_description').val());
        product_data.push($('#product_stock').val());
        product_data.push($('#product_cost_price').val());
        // fieldValues.push($('#discount_description').val());
        product_data.push($('#product_selling_price').val());
        product_data.push($('#product_vendor').val());
        product_data.push($('#product_category').val());
        
        var url_link = (typeof product_id === 'undefined') ? '/save_product' : '/save_product/' + product_id;
        product_sub_unit(url_link, product_data)
        }
    }
    
function product_sub_unit(url_link, product_data) {
    var table = $('#tbl__body');
    var rows = table.find('tr');
    var unit_data = [];
    
    rows.each(function() {
        var row = $(this);
        var unit = row.find('.tbl_unit select').val();
        var multiple = row.find('.tbl_multiple select').val();
        var multiple_value = row.find('.tbl_multiple_value').text().trim();

        unit_data.push([unit, multiple, multiple_value]);
    });

    var data = {
        product_data: product_data,
        unit_data: unit_data
    };

    // Use Axios for the AJAX request
    axios.post(url_link, JSON.stringify(data), {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // You need a function to get the CSRF token
        }
        })
        .then(response => {
            $('#form__btn-submit').closest('form').submit();
        })
        .catch(error => {
            console.error('Error in Axios request:', error);
    });
}

function formSearch() {
    row = $("#tbl__body");
    rowCounter = 1;
    row.html('');
    search_val = $('#formSearch').val();
    if (search_val === '' || search_val === undefined) {
        findRow(`form_search/tblProduct`, row);
        return;
    }
    search_in = $('#cmbFormSearch').val();
    switch(search_in) {
        case 'product_code':
            findRow(`form_search/tblProduct/product_code/` + search_val, row);
            break;
        case 'product_name':
            findRow(`form_search/tblProduct/product_name/` + search_val, row);
            break;
        case 'vendor_name':
            findRow(`form_search/tblProduct/vendor__vendor_name/` + search_val, row);
            break;
        case 'category_name':
            findRow(`form_search/tblProduct/category__category_name/` + search_val, row);
            break;
        default:
            findRow(`form_search/tblProduct/` + search_val, row);
  }
}

function findRow(url_link, row) {
    rowCounter = 1;
    axios.get(url_link)
    .then(response => {
        response.data.forEach(item => {
            new_row = '<tr class="form-list__contents">' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + rowCounter + '</p></td>' +
                '<td class="py-2"><a href="/product/' + item.id + '"><p class="text-black font-semibold text-base">' + item.product_name + '</p></a></td>' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + item.main_unit + '</p></td>' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + item.cost_price + '</p></a></td>' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + item.stock + '</p></td>' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + item.vendor_name + '</p></td>' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + item.category_name + '</p></td>' +
                '</tr>';

            row.append(new_row);
            rowCounter++;
        })
    })
    .catch(error => {
        console.error('Error in Axios request:', error);
    });
  }


$(document).ready(function() {
    $('#tbl__body').on('keypress', '.num-only', function(e) {
        acceptNum(this, e); 
        
    });

    $('#tbl__body').on('blur', '.tbl_unit', function() {
        // const row = $(this).closest('tr');
        // const rowCounter = parseInt(row.attr('id').replace('row', ''), 10);
        // const totalRows = $('#tbl__body tr').length;
        // if (!$(this).val()) {
        //     if(totalRows > 1) {
        //         row.remove();
        //         // rearrange(row.attr('id'))
        //     } else if (totalRows == 1) {
        //         $('#sub_unit').prop('checked', false);
        //         $('#sub_unit').val(0);
        //         $('#form__tbl').hide();
        //     }
        //     $('#product_name').focus();
        // }
    });

    $('#tbl__body').on('blur', '.tbl_multiple_value', function() {
        const row = $(this).closest('tr');
        const rowCounter = parseInt(row.attr('id').replace('row', ''), 10);
        const totalRows = $('#tbl__body tr').length;
        if (!$(this).text()) {
            $(this).text('0');
        }
    });

    $('#tbl__body').on('keydown', '.tbl_multiple_value', function(event) {
        const row = $(this).closest('tr');
        const totalRows = $('#tbl__body tr').length;
        if ((event.key === 'Enter' || event.key === 'Tab') && row.is(':last-child') && !event.shiftKey && $('#tbl_unit_' + totalRows).val()) {
            event.preventDefault(); // Prevent the default behavior (e.g., moving to the next cell)
            
            
            const rowNo = totalRows + 1;
            // console.log(rowNo);
            
            const newRow = `<tr class="form__details-contents" id="row${rowNo}">
                <td class="py-2 tbl_sl" id="tbl_sl_${rowNo}">${rowNo}</td>
                <td class="py-2 tbl_unit">
                <select id="tbl_unit_${rowNo}">
                    <option value=""></option>
                    <option value="box">Box</option>
                    <option value="num">Num</option>
                    <option value="ctn">Ctn</option>
                </select>
                </td>
                <td class="py-2 tbl_multiple">
                <select id="tbl_multiple_${rowNo}">
                    <option value="*">*</option>
                    <option value="/">/</option>
                </select>
                </td>
                <td class="py-2 tbl_multiple_value num-only" contenteditable="true" id="tbl_multiple_value_${rowNo}"></td>
            </tr>`;
            
            $("#form__tbl tbody").append(newRow);
            $('#tbl_unit_' + rowNo).focus();
        } else if ((event.key === 'Enter' || event.key === 'Tab') && row.is(':last-child') && !event.shiftKey && !$('#tbl_unit_' + totalRows).val() && !row.is(':first-child')) {
            row.remove();
        } else if ((event.key === 'Enter' || event.key === 'Tab') && !event.shiftKey && !$('#tbl_unit_' + totalRows).val() && totalRows == 1) {
            $('#sub_unit').prop('checked', false);
            $('#sub_unit').val(0);
            $('#form__tbl').hide();
        }
    });
            
    $('#sub_unit').change(function(){
        if($(this).is(":checked")) {
            $('#form__tbl').show();
        } else {
            $('#form__tbl').hide();
        }
    });

    $('#product_vendor_name').on('blur', function() {
        vendor = $(this).val();
        axios.get('/get_field_details/tblVendor/vendor_code/vendor_name/' + vendor)
        .then(response => {
            value = response.data;
            if (vendor == value.vendor_code) {
                $(this).val(value.vendor_name);
                $('#product_vendor').val(value.id)
            }
            else if (vendor != value.vendor_name) {
                $(this).val('Enter a valid vendor code/name');
            }
            else {
                $('#product_vendor').val(value.id)
            }
        })
    })
    
    $('#product_category_name').on('blur', function() {
        category = $(this).val();
        axios.get('/get_field_details/tblCategory/category_code/category_name/' + category)
        .then(response => {
            value = response.data;
            if (category == value.category_code) {
                $(this).val(value.category_name);
                $('#product_category').val(value.id)
            }
            else if (category != value.category_name) {
                $(this).val('Enter a valid category code/name');
            }
            else {
                $('#product_category').val(value.id)
            }
        })
    })
});