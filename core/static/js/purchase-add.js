function tblTotal(rowCounter) {
    const qty =  parseInt($('#tbl_qty_' + rowCounter).text()) || 0;
    const price =  parseFloat($('#tbl_price_' + rowCounter).text()) || 0;
    const vat_perc =  parseFloat($('#tbl_vat_perc_' + rowCounter).text()) || 0;
    const discount =  parseFloat($('#tbl_discount_' + rowCounter).text()) || 0;
    const vat = decimal_2((qty * price - discount) * (vat_perc / 100));

    $('#tbl_vat_' + rowCounter).text(vat);

    total = qty * price + vat - discount;
    $('#tbl_total_' + rowCounter).text(decimal_2(total));
    updateTotal();
}

function updateTotal() {
    let vat = 0;
    let discount = 0;
    let total = 0;
    $(".tbl_vat").each(function () {
      const vat_amt = parseFloat($(this).text());
      if (!isNaN(vat_amt)) {
        vat += vat_amt;
      }
    });
    
    $(".tbl_discount").each(function () {
      const disc = parseFloat($(this).text());
      if (!isNaN(disc)) {
        discount += disc;
      }
    });
    
    $(".tbl_total").each(function () {
      const totalAmount = parseFloat($(this).text());
      if (!isNaN(totalAmount)) {
        total += totalAmount;
      }
    });
    // Update the total amount field with the calculated sum
    $("#master_vat").val(decimal_2(vat));
    $("#master_discount").val(decimal_2(discount));
    $("#master_total").val(decimal_2(total + discount - vat));
    updateNetAmount();
}
  
function updateNetAmount() {
    const total = parseFloat($("#master_total").val()) || 0;
    const discount = parseFloat($("#master_discount").val()) || 0;
    const vat = parseFloat($("#master_vat").val()) || 0;
    const roundOff = parseFloat($("#master_roundoff").val()) || 0;
  
    net = decimal_2(total - discount + vat + roundOff);
    $("#master_net_amount").val(net);
    balanceAmount();
}
  
function balanceAmount() {
    const receivedAmount = parseFloat($("#master_amount_payed").val()) || 0;
    const netAmount = parseFloat($("#master_net_amount").val()) || 0;
  
    amount = decimal_2(netAmount - receivedAmount);
    $("#master_balance").val(amount);
}

function save_purchase(event, purchase_id) {
    event.preventDefault();
    
    if (is_field_empty('#master_vendor_code', 'Please enter a valid vendor code')) {
        return;
    } else if ($('#tbl_product_1').text() === null || $('#tbl_product_1').text() === '') {
        alert('no products added in this invoice')
        $('#tbl_product_1').focus();
        return;
    } else {
        vendor_id = $('#master_vendor_id').val() || 0;
        does_field_exist('tblVendor', 'id', vendor_id)
            .then(result => {
                if (!result) {
                    alert('Please enter a valid vendor code');
                    $('#master_vendor_id').focus();
                    return;
                }
                
                // Create an array to store the field values
                var master_data = [];
            
                // Retrieve and store the values of each field
                master_data.push($('#master_invoice_no').val());
                master_data.push($('#master_purchase_no').val());
                // master_data.push(date_to_yyyymmdd('#master_invoice_date'));
                master_data.push($('#master_invoice_date').val());
                master_data.push($('#master_total').val());
                master_data.push($('#master_vat').val());
                master_data.push($('#master_discount').val());
                // fieldValues.push($('#discount_description').val());
                master_data.push($('#master_roundoff').val());
                master_data.push($('#master_net_amount').val());
                master_data.push($('#master_amount_payed').val());
                master_data.push($('#master_balance').val());
                master_data.push($('#master_payment_method').val());
                master_data.push($('#master_vendor_id').val());
                master_data.push($('#master_salesman_id').val());

                var url_link = (typeof purchase_id === 'undefined') ? '/save_purchase' : '/save_purchase/' + purchase_id;
                purchase_details(url_link, master_data)
                
            })
            .catch(error => {
                console.error('Error checking field existence:', error);
            });
    }
}

function purchase_details(url_link, master_data) {
    var table = $('#tbl__body');
    var rows = table.find('tr');
    var details_data = [];
  
    rows.each(function() {
      var row = $(this);
      var values = row.find('td').map(function() {
        return $(this).text();
      }).get();
      values[4] = row.find('.tbl_unit select').val();
      details_data.push(values);
    });
  
    var data = {
      master_data: master_data,
      details_data: details_data
    };
  
    // Use Axios for the AJAX request
    axios.post(url_link, JSON.stringify(data), {
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // You need a function to get the CSRF token
        }
        })
        .then(response => {
            console.log(response);
            $('#form__btn-submit').closest('form').submit();
        })
        .catch(error => {
            console.error('Error in Axios request:', error);
        });
}
  


function findRow(url_link, row) {
    rowCounter = 0;
    axios.get(url_link)
    .then(response => {
        response.data.forEach(item => {
            // Use item.id, item.purchase_no, etc.
            new_row = '<tr class="form-list__contents">' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + rowCounter + '</p></td>' +
                '<td class="py-2"><a href="/purchase/' + item.id + '"><p class="text-black font-semibold text-base">' + item.id + '</p></a></td>' +
                '<td class="py-2"><a href="/purchase/' + item.id + '"><p class="text-black font-semibold text-base">' + item.purchase_no + '</p></a></td>' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + item.invoice_date + '</p></td>' +
                '<td class="py-2"><a href="/purchase/' + item.id + '"><p class="text-black font-semibold text-base">' + item.vendor_name + '</p></a></td>' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + item.discount + '</p></td>' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + item.net_amount + '</p></td>' +
                '<td class="py-2"><p class="text-black font-semibold text-base">' + item.balance + '</p></td>' +
                '</tr>';

            row.append(new_row);
            rowCounter++;
        })
    })
    .catch(error => {
        console.error('Error in Axios request:', error);
    });
}

//rearrange_row()

$(document).ready(function() {
    $('#master_vendor_code').on('input', function() {
        let vendorCode = $(this).val().trim() || 0;
        // axios(`/get_field_details/tblVendor/vendor_code/${vendorCode}`)
        // .then(response => {
        //     value = response.data.results[0]
        //     if (value.id) {
        //         $(`#master_vendor_id`).val(value.id);
        //         $(`#master_vendor_name`).val(value.vendor_name);
        //     } else {
        //         $(`#master_vendor_id`).val('');
        //         $(`#master_vendor_name`).val('');
        //     }
        // })
        // .catch(error => {
        //     $(`#master_vendor_id`).val('');
        //     $(`#master_vendor_name`).val('');
        // })      
        row = $("#form__suggestion");
        rowCounter = 1;
        row.html('');
        if (vendorCode === '' || vendorCode === undefined) {
            return;
        }
        axios.get(`form_search/tblVendor/vendor_code/vendor_name/` + vendorCode)
        .then(response => {
            response.data.forEach(item => {
                // Use item.id, item.purchase_no, etc.
                new_row = `<button id="suggestion__btn_${rowCounter}" class="suggestion__btn" type="button">${item.vendor_name}</button>`;

                row.append(new_row);
                rowCounter++;
            })
        })
    })

    $('#master_vendor_code').on('blur', function() {
        let vendorCode = $(this).val().trim() || 0;
        axios.get(`form_search/tblVendor/vendor_code/vendor_name/` + vendorCode)
        .then(response => {
            response.data.forEach(item => {
                // Use item.id, item.purchase_no, etc.
                new_row = `<button id="suggestion__btn_${rowCounter}" class="suggestion__btn" type="button">${item.vendor_name}</button>`;

                row.append(new_row);
                rowCounter++;
            })
        })
    })

    $('#master_salesman_code').on('input', function() {
        let salesmanCode = $(this).val().trim() || 0;
        axios(`/get_field_details/tblEmployee/employee_code/${salesmanCode}`)
        .then(response => {
            value = response.data.results[0]
            if (value.id) {
                $(`#master_salesman_id`).val(value.id);
                $(`#master_salesman_name`).val(value.employee_name);
            } else {
                $(`#master_salesman_id`).val('');
                $(`#master_salesman_name`).val('');
            }
        })
        .catch(error => {
            $(`#master_salesman_id`).val('');
            $(`#master_salesman_name`).val('');
        })      
    })

    $('#tbl__body').on('input', 'td[id^="tbl_"][contenteditable="true"]', function() {
        const row = $(this).closest('tr');
        const rowCounter = parseInt(row.attr('id').replace('row', ''), 10);
        const first_columnName = $(this).attr('id').replace(`tbl_`, '');
        const columnName = first_columnName.replace(`_${rowCounter}`, '');
        // Check which column is being edited
        switch (columnName) {
            case 'product':
                let productCode = $(this).text().trim().toUpperCase() || '0';

                axios.get(`/get_field_details/tblProduct/product_code/product_name/${productCode}`)
                .then(response => {
                    value = response.data.results[0]
                        if (value.id) {
                            $(`#tbl_product_id_${rowCounter}`).text(value.id);
                            // $(`#tbl_product_${rowCounter}`).text(value.product_name);
                            $(`#tbl_unit_${rowCounter}`).append((`<option value="${value.main_unit}">${value.main_unit}</option>`));
                            axios.get(`/get_field_details/tblCategory/id/${value.category_id}`)
                            .then(result => {
                                $(`#tbl_vat_perc_${rowCounter}`).text(result.data.results[0].vat_rate);
                            })
                            .catch(error => {
                                console.log(error)
                            })
                            axios.get(`/get_field_details/tblProduct_unit/product/${value.id}`)
                            .then(result => {
                                result.data.results.forEach(item => {
                                    $(`#tbl_unit_${rowCounter}`).append((`<option value="${item.unit}">${item.unit}</option>`));
                                });
                            })
                            .catch(error => {
                                // console.log(error)
                            })
                        } else {
                            $(`#tbl_product_id_${rowCounter}`).text('');
                            $(`#tbl_vat_perc_${rowCounter}`).text('');
                            $(`#tbl_unit_${rowCounter}`).empty();
                        }
                    })
                    .catch(error => {
                        $(`#tbl_product_id_${rowCounter}`).text('');
                        $(`#tbl_vat_perc_${rowCounter}`).text('');
                        $(`#tbl_unit_${rowCounter}`).empty();
                    })
                break;
            case 'qty':
                tblTotal(rowCounter);
                break;
            case 'price':
                tblTotal(rowCounter);
                break;
            case 'discount':
                tblTotal(rowCounter);
                break;
        }
    });

    $('#tbl__body').on('focus', 'td[contenteditable="true"]', function() {
        var range = document.createRange();
        range.selectNodeContents(this);

        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
    });

    $('#tbl__body').on('blur', '.tbl_product', function() {
        const row = $(this).closest('tr');
        const rowCounter = parseInt(row.attr('id').replace('row', ''), 10);
        const totalRows = $('#tbl__body tr').length;
        if ($(this).text() === '') {
            if(totalRows > 1 && !row.is(':last-child')) {
                row.remove();
                rearrange(row.attr('id'))
                updateTotal();
                // setTimeout(() => {
                    // $('#tbl_discount_' + (rowCounter-1)).focus();
                    // }, 0.5);
                $('#tbl_product_' + (rowCounter+1)).focus();
                }
                else if (totalRows == 1) {
                    $('#form__btn-cancel').focus();
                }
        }
        else {
            productId = $(`#tbl_product_id_${rowCounter}`).text() || 0;
            axios.get(`/get_field_details/tblProduct/id/${productId}`)
            .then(response => {
                value = response.data.results[0]
                    if (value.id) {
                        $(`#tbl_product_${rowCounter}`).text(value.product_name)
                    } else {
                        $(`#tbl_product_id_${rowCounter}`).text('');
                        $(`#tbl_vat_perc_${rowCounter}`).text('');
                        $(`#tbl_unit_${rowCounter}`).empty();
                        toast_message("Invalid product code")
                        setTimeout(() => {
                            $("#tbl_product_" + rowCounter).focus();
                        }, 0.5);
                    }
                })
                .catch(error => {
                    $(`#tbl_product_id_${rowCounter}`).text('');
                        $(`#tbl_vat_perc_${rowCounter}`).text('');
                        $(`#tbl_unit_${rowCounter}`).empty();
                        toast_message("Invalid product code")
                        setTimeout(() => {
                            $("#tbl_product_" + rowCounter).focus();
                        }, 0.5);
                    // console.error('Error checking field existence:', error);
                })
        }
    });
    

    $('#tbl__body').on('keydown', 'td[id^="tbl_"][contenteditable="true"]', function(event) {
        const row = $(this).closest('tr');
        const rowCounter = parseInt(row.attr('id').replace('row', ''), 10);
        const totalRows = $('#tbl__body tr').length;
        const first_columnName = $(this).attr('id').replace(`tbl_`, '');
        const columnName = first_columnName.replace(`_${rowCounter}`, '');
        // Check which column is being edited
        switch (columnName) {
            case 'product':
                if ((event.key === 'Enter' || event.key === 'Tab') && (!$(this).text() || $(this).text() === undefined) && totalRows >1 && row.is(':last-child')) {
                    event.preventDefault();
                    if (event.shiftKey){
                        $('#tbl_discount_' + (rowCounter - 1)).focus();
                    }
                    else {
                        $('#form__btn-submit').focus();
                    }
                    row.remove();
                    rearrange(row.attr('id'));
                    updateTotal();
                }
                else if (event.key === 'Enter') {
                    event.preventDefault();
                    if (event.shiftKey) {
                        if (row.is(':first-child')) {
                            $('#form__btn-cancel').focus();
                        } else {
                            $('#tbl_discount_' + (rowCounter - 1)).focus();
                        }
                    } else {
                        $('#tbl_qty_' + rowCounter).focus();
                    }
                }
                    
                break;

            case 'qty':
                if (event.key === 'Enter') {
                    event.preventDefault();
                    if (event.shiftKey) {
                        $('#tbl_product_' + rowCounter).focus();
                    } else {
                        $('#tbl_price_' + rowCounter).focus();
                    }
                } 
                // else if (event.key === 'Tab' && !event.shiftKey) {
                //     event.preventDefault();
                //     $('#tbl_price_' + rowCounter).focus();
                // }
                break;
        
            case 'price':
                if (event.key === 'Enter') {
                    event.preventDefault();
                    if (event.shiftKey) {
                        $('#tbl_qty_' + rowCounter).focus();
                    } else {
                        $('#tbl_discount_' + rowCounter).focus();
                    }
                } 
                // else if (event.key === 'Tab' && !event.shiftKey) {
                //     event.preventDefault();
                //     $('#tbl_discount_' + rowCounter).focus();
                // }
                break;
        
            case 'discount':
                if ((event.key === 'Enter' || event.key === 'Tab') && row.is(':last-child') && !event.shiftKey) {
                    event.preventDefault(); // Prevent the default behavior (e.g., moving to the next cell)


                    const rowNo = totalRows + 1;
                    // console.log(rowNo);

                    const newRow = `<tr class="form__details-contents" id="row${rowNo}">
                        <td class="py-2 tbl_sl" id="tbl_sl_${rowNo}">${rowNo}</td>
                        <td class="py-2 tbl_product uppercase-only" contenteditable="true" id="tbl_product_${rowNo}"></td>
                        <td class="py-2 tbl_product_id" id="tbl_product_id_${rowNo}" hidden></td>
                        <td class="py-2 tbl_unit">
                            <select id="tbl_unit_${rowNo}">
                                <option value="option"></option>
                            </select>
                        </td>
                        <td class="py-2 tbl_qty" contenteditable="true" id="tbl_qty_${rowNo}"></td>
                        <td class="py-2 tbl_price" contenteditable="true" id="tbl_price_${rowNo}"></td>
                        <td class="py-2 tbl_vat_perc" id="tbl_vat_perc_${rowNo}"></td>
                        <td class="py-2 tbl_vat" id="tbl_vat_${rowNo}"></td>
                        <td class="py-2 tbl_discount" contenteditable="true" id="tbl_discount_${rowNo}"></td>
                        <td class="py-2 tbl_total" id="tbl_total_${rowNo}"></td>
                    </tr>`;

                    $("#form__tbl tbody").append(newRow);
                    $('#tbl_product_' + rowNo).focus();
                // } else if (event.key === 'Enter' || event.which === 13 || event.code === 'NumpadEnter') {
                } else if (event.key === 'Enter') {
                    event.preventDefault();
                
                    if (event.shiftKey) {
                        // console.log('Shift + Enter pressed');
                        $('#tbl_price_' + rowCounter).focus();
                    } else {
                        // console.log('Enter pressed');
                        $('#tbl_product_' + (rowCounter + 1)).focus();
                    }
                }
                break;
        }
    });

    $('#master_roundoff').on('input', function() {
        value = parseFloat($('#master_roundoff').val())
        if (value < -1) {
          $('#master_roundoff').val(-1)
        }
        else if(value>1) {
          $('#master_roundoff').val(1)
        }
        updateNetAmount();
    })

    $('#master_amount_payed').on('input', function() {
        balanceAmount();
    })

    $('#formSearch').on('input', function() {
        row = $("#tbl__body");
        rowCounter = 1;
        row.html('');
        search_val = $('#formSearch').val();
        if (search_val === '' || search_val === undefined) {
            findRow(`form_search/tblPurchase_Master`, row);
            return;
        }
        search_in = $('#cmbFormSearch').val();
        switch(search_in) {
            case 'invoice_no':
                findRow(`form_search/tblPurchase_Master/id/` + search_val, row);
                break;
            case 'purchase_no':
                findRow(`form_search/tblPurchase_Master/purchase_no/` + search_val, row);
                break;
            case 'vendor_name':
                findRow(`form_search/tblPurchase_Master/vendor__vendor_name/` + search_val, row);
                break;
            case 'invoice_date':
                findRow(`form_search/tblPurchase_Master/invoice_date/` + search_val, row);
                break;
            default:
                findRow(`form_search/tblPurchase_Master/` + search_val, row);
        }
    });
});


// replaceChildIds(row);
// function replaceChildIds(row) {
//     const cells = $(row).find('td');
  
//       cells.each(function() {
//         const colId = $(this).attr('id');
//         const value = getAlphabeticAndNumericValues(colId); 
//         const newColId = value.alphabetic.replace(',', '') + (parseInt(value.numeric));
//         $(this).attr('id', newColId);
//         console.log(newColId)
//       });
//   }

//   function getAlphabeticAndNumericValues(text) {
//     const alphabeticRegex = /[a-z_]/gi;
//     const numericRegex = /\d/gi;
  
//     return {
//         alphabetic: (text.match(alphabeticRegex) || []).join(''), // Ensure it's an array and join
//         numeric: (text.match(numericRegex) || []).join(''), // Ensure it's an array and join
//     };
//   }