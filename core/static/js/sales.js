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
  const receivedAmount = parseFloat($("#master_amount_received").val()) || 0;
  const netAmount = parseFloat($("#master_net_amount").val()) || 0;

  amount = decimal_2(netAmount - receivedAmount);
  $("#master_balance").val(amount);
}

function unit_stock_change(index) {
  var selected = $(`#tbl_unit_${index}`).find("option:selected");
  var stock = $(`#tbl_stock_${index}`).text();
  var operator = selected.next().val();
  var operand = selected.next().next().val();
  if (operator === "#") {
    $(`#tbl_stock_${index}`).text(operand);
  }
  else {
    stock = $(`#tbl_unit_${index}`).find("option:eq(2)").val()
    if (operator === "*") {
      $(`#tbl_stock_${index}`).text(decimal_2(stock) * decimal_2(operand));
    }
    else {
      $(`#tbl_stock_${index}`).text(decimal_2(stock) / decimal_2(operand));
    }
  }
}

function save_orderOrDelivery(event, orderOrDelivery, id) {
  event.preventDefault();
  
  if (is_field_empty('#master_customer', 'Invalid customer')) {
      return;
  } else if ($('#tbl_product_1').text() === null || $('#tbl_product_1').text() === '') {
      toast_message('no products added in this invoice')
      $('#tbl_product_1').focus();
      return;
  } else {
      customer_id = $('#master_customer_id').val() || 0;
      does_field_exist('tblCustomer', 'id', customer_id)
      .then(result => {
        if (!result) {
          toast_message('Invalid customer');
          $('#master_customer_id').focus();
          return;
        }
        
        // Create an array to store the field values
        var master_data = [];
        // Retrieve and store the values of each field
        if (orderOrDelivery == 'order') {
          master_data.push($('#master_order_no').val());
          master_data.push($('#master_order_date').val());
        }
        else {
          master_data.push($('#master_delivery_note_no').val());
          master_data.push($('#master_delivery_note_date').val());
        }
        master_data.push($('#master_total').val());
        master_data.push($('#master_vat').val());
        master_data.push($('#master_discount').val());
        master_data.push($('#master_roundoff').val());
        master_data.push($('#master_net_amount').val());
        master_data.push($('#master_customer_id').val());
        master_data.push($('#master_salesman_id').val());

        var url_link = id? `/save_${(orderOrDelivery === 'order')?`salesOrder`:`deliveryNote`}/` + id : `/save_${(orderOrDelivery === 'order')?`salesOrder`:`deliveryNote`}`;
        sales_details(url_link, master_data, false)
      })
      .catch(error => {
          console.error('Error checking field existence:', error);
      });
  }
}

function save_sales(event, returnSales, sales_id) {
  event.preventDefault();
  
  if (is_field_empty('#master_customer', 'Invalid customer')) {
      return;
  } else if ($('#tbl_product_1').text() === null || $('#tbl_product_1').text() === '') {
      toast_message('no products added in this invoice')
      $('#tbl_product_1').focus();
      return;
  } else {
      customer_id = $('#master_customer_id').val() || 0;
      does_field_exist('tblCustomer', 'id', customer_id)
      .then(result => {
        if (!result) {
          toast_message('Invalid customer');
          $('#master_customer_id').focus();
          return;
        }
        
        // Create an array to store the field values
        var master_data = [];
        // Retrieve and store the values of each field
        master_data.push($('#master_invoice_no').val());
        if (returnSales) {
          master_data.push($('#master_return_no').val());
        }
        else {
          master_data.push('');
        }
        master_data.push($('#master_invoice_date').val());
        master_data.push($('#master_total').val());
        master_data.push($('#master_vat').val());
        master_data.push($('#master_discount').val());
        master_data.push($('#master_roundoff').val());
        master_data.push($('#master_net_amount').val());
        master_data.push($('#master_amount_received').val());
        master_data.push($('#master_balance').val());
        master_data.push($('#master_payment_method').val());
        master_data.push($('#master_customer_id').val());
        master_data.push($('#master_salesman_id').val());

        var url_link = (typeof sales_id === 'undefined') ? '/save_sales' : '/save_sales/' + sales_id;
        sales_details(url_link, master_data, returnSales)
      })
      .catch(error => {
          console.error('Error checking field existence:', error);
      });
  }
}

function sales_details(url_link, master_data, returnSales) {
  var table = $('#tbl__body');
  var rows = table.find('tr');
  var details_data = [];

  rows.each(function() {
    var row = $(this);
    var values = row.find('td').map(function() {
      return $(this).text();
    }).get();
    values[3] = row.find('.tbl_unit select').val();
    details_data.push(values);
    if (returnSales)
      values.splice(4, 0, '');
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
      $('#form__btn-submit').closest('form').submit();
  })
  .catch(error => {
      console.error('Error in Axios request:', error);
  });
}

function formSearch(returnSales=false) {
  row = $("#tbl__body");
  rowCounter = 1;
  row.html('');
  search_val = $('#formSearch').val();
  if (search_val === '' || search_val === undefined) {
    findRow(`form_search/tblSales_Master`, row, returnSales);
    return;
  }
  search_in = $('#cmbFormSearch').val();
  switch(search_in) {
      case 'invoice_no':
          findRow(`form_search/tblSales_Master/invoice_no/` + search_val, row, returnSales);
          break;
      case 'customer_name':
          findRow(`form_search/tblSales_Master/customer__customer_name/` + search_val, row, returnSales);
          break;
      case 'invoice_date':
        findRow(`form_search/tblSales_Master/invoice_date/` + search_val, row, returnSales);
        break;
      case 'return_no':
          findRow(`form_search/tblSales_Master/return_no/` + search_val, row, returnSales);
          break;
      default:
          findRow(`form_search/tblSales_Master/` + search_val, row, returnSales);
  }
}

function findRow(url_link, row, returnSales) {
  rowCounter = 1;
  axios.get(url_link)
  .then(response => {
      response.data.forEach(item => {
        if (returnSales? item.return_no > 0:item.return_no == 0) {
          new_row = '<tr class="form-list__contents">' +
          '<td class="py-2"><p class="text-black font-semibold text-base">' + rowCounter + '</p></td>' +
          (returnSales? '<td class="py-2"><a href="/sales/' + item.id + '"><p class="text-black font-semibold text-base">' + item.return_no + '</p></a></td>':'') +
          '<td class="py-2"><a href="/sales/' + item.id + '"><p class="text-black font-semibold text-base">' + item.invoice_no + '</p></a></td>' +
          '<td class="py-2"><p class="text-black font-semibold text-base">' + item.invoice_date + '</p></td>' +
          '<td class="py-2"><a href="/sales/' + item.id + '"><p class="text-black font-semibold text-base">' + item.customer_name + '</p></a></td>' +
          '<td class="py-2"><p class="text-black font-semibold text-base">' + item.net_amount + '</p></td>' +
          '<td class="py-2"><p class="text-black font-semibold text-base">' + item.balance + '</p></td>' +
          (returnSales? '':'<td class="py-2"><p class="text-black font-semibold text-base">Due Date</p></td>') +
          '</tr>';
          
          row.append(new_row);
          rowCounter++;
        }
      })
  })
  .catch(error => {
      console.error('Error in Axios request:', error);
  });
}

//rearrange_row()

$(document).ready(function() {
  $('#master_customer').on('blur', function() {
    let customerCode = $(this).val().trim() || 0;
    axios(`/get_field_details/tblCustomer/customer_code/customer_name/${customerCode}`)
    .then(response => {
        value = response.data.results[0]
        if (value.id) {
            $(`#master_customer_id`).val(value.id);
            $(`#master_customer`).val(value.customer_name);
        } else {
            $(`#master_customer_id`).val('');
            toast_message('Invalid customer');
          }
        })
        .catch(error => {
          $(`#master_customer_id`).val('');
          toast_message('Invalid customer');
        })      
      })
      
      $('#master_salesman').on('blur', function() {
        let salesmanCode = $(this).val().trim() || 0;
        axios(`/get_field_details/tblSalesman/salesman_code/salesman_name/${salesmanCode}`)
        .then(response => {
          value = response.data.results[0]
          if (value.id) {
            $(`#master_salesman_id`).val(value.id);
            $(`#master_salesman`).val(value.salesman_name);
          } else {
            $(`#master_salesman_id`).val('');
            toast_message('Invalid salesman');
          }
        })
        .catch(error => {
          $(`#master_salesman_id`).val('');
          toast_message('Invalid salesman');
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
          break;
      case 'qty':
        break;
      case 'price':
          tblTotal(rowCounter);
          break;
      case 'discount':
          tblTotal(rowCounter);
          break;
  }
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
    let productCode = $(this).text().trim().toUpperCase() || '0';
    axios.get(`/get_field_details/tblProduct/product_code/product_name/${productCode}`)
    .then(response => {
    value = response.data.results[0]
    console.log(value);
    if (value.id) {
        $(`#tbl_product_id_${rowCounter}`).text(value.id);
        $(`#tbl_product_${rowCounter}`).text(value.product_name);
        $(`#tbl_unit_${rowCounter}`).empty();
        $(`#tbl_unit_${rowCounter}`).append((`<option value="${value.main_unit}">${value.main_unit}</option>`));
        $(`#tbl_unit_${rowCounter}`).append((`<option value="#" hidden>#</option>`));
        $(`#tbl_unit_${rowCounter}`).append((`<option value="${value.stock}" hidden>${value.stock}</option>`));
        $(`#tbl_stock_${rowCounter}`).text(value.stock);
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
            $(`#tbl_unit_${rowCounter}`).append((`<option value="${item.multiple}" hidden>${item.multiple}</option>`));
            $(`#tbl_unit_${rowCounter}`).append((`<option value="${item.multiple_value}" hidden>${item.multiple_value}</option>`));
            });
        })
        .catch(error => {
            // console.log(error)
        })
    } else {
      $(`#tbl_product_${rowCounter}`).focus();
      toast_message("Invalid product")
        $(`#tbl_product_id_${rowCounter}`).text('');
        $(`#tbl_vat_perc_${rowCounter}`).text('');
        $(`#tbl_unit_${rowCounter}`).empty();
        $(`#tbl_stock_${rowCounter}`).text('');
      }
    })
    .catch(error => {
      $(`#tbl_product_${rowCounter}`).focus();
      toast_message("Invalid product")
      $(`#tbl_product_id_${rowCounter}`).text('');
      $(`#tbl_vat_perc_${rowCounter}`).text('');
      $(`#tbl_unit_${rowCounter}`).empty();
      $(`#tbl_stock_${rowCounter}`).text('');
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
          break;
  
      case 'discount':
          if ((event.key === 'Enter' || event.key === 'Tab') && row.is(':last-child') && !event.shiftKey) {
              event.preventDefault();


              const rowNo = totalRows + 1;
              // console.log(rowNo);

              const newRow = `<tr class="form__details-contents" id="row${rowNo}">
                  <td class="py-2 tbl_sl" id="tbl_sl_${rowNo}">${rowNo}</td>
                  <td class="py-2 tbl_product uppercase-only" contenteditable="true" id="tbl_product_${rowNo}"></td>
                  <td class="py-2 tbl_product_id" id="tbl_product_id_${rowNo}" hidden></td>
                  <td class="py-2 tbl_unit">
                      <select id="tbl_unit_${rowNo}" onchange=(unit_stock_change(${rowNo}))>
                      </select>
                  </td>` + ($('.tbl_stock').length > 0? `<td class="py-2 tbl_stock" id="tbl_stock_${rowNo}"></td>`:``) + 
                  `<td class="py-2 tbl_qty" oninput="qtyChange(${rowNo})" contenteditable="true" id="tbl_qty_${rowNo}"></td>
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
                  $('#tbl_price_' + rowCounter).focus();
              } else {
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
});