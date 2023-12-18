document.addEventListener('DOMContentLoaded', function () {
  const disabledInputs = document.querySelectorAll('.disabled-input');

  // Loop through the disabled input fields and set the tabindex to -1
  disabledInputs.forEach(function(input) {
    input.tabIndex = -1;
  });

  $('#tbl__body').on('focus', 'td[contenteditable="true"]', function() {
    var range = document.createRange();
    range.selectNodeContents(this);

    var selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
});
});

const is_field_empty = (field_id, msg) => {
  if (($(field_id).val() === null || $(field_id).val() === '')) {
    if (msg) {
      toast_message(msg);
    }
    // Focus on the empty field
    $(field_id).focus();
    
    // Return false to indicate that the field is empty
    return true;
  }
  
  // Return true if the field is not empty
  return false;
}

const does_field_exist = (tbl_name, tbl_field, field_value) => {
  return axios.get(`/does_field_exist/${tbl_name}/${tbl_field}/${field_value}`)
        .then(response => response.data.result)
        .catch(error => {
            console.error('Error checking field existence:', error);
            throw new Error('Error checking field existence');
        });
};

const decimal_2 = (value) => {
  return Math.round(value * 100) / 100;
}


function rearrange(id) {
  var idValue = parseInt(id.replace('row', ''), 10);
  const rows = $('#tbl__body tr').toArray();
  // Sort the rows based on idValue
  rows.sort((a, b) => {
    const aIdValue = parseInt($(a).attr('id').replace('row', ''), 10);
    const bIdValue = parseInt($(b).attr('id').replace('row', ''), 10);
    return aIdValue - bIdValue;
  });
  
  // Rearrange the rows sequentially
  rows.forEach(function(row) {
      const rowIdValue = parseInt($(row).attr('id').replace('row', ''), 10);

      if (rowIdValue > idValue) {
          
          // Update the row ID
          $(row).attr('id', 'row' + idValue);
          
          // Update other IDs within the row
          $(row).find('[id^="tbl_"]').each(function() {
              const oldId = $(this).attr('id');
              const newId = oldId.replace(rowIdValue, idValue);
              $(this).attr('id', newId);
          });
          
          // Update the displayed row number
          $(row).find('td:first-child').text(idValue);
          idValue++;
      }
      
  });
}

function acceptNum(current_id, event) {
  if (!/[0-9]/.test(event.key) && $(current_id).text().includes('.')) {
    event.preventDefault();
  }
  else if (!/[0-9.]/.test(event.key)) {
      event.preventDefault();
  }
}


// Function to get CSRF token from cookies
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
}


function toast_message(message) {
  $('body').append(
    `<dialog id="toast_modal" class="toast-modal" open style='margin: 0 auto;width: 25rem;bottom: 10px;z-index:100;border-radius:15px;box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);text-align:center;'>
        ${message}<br />
    </dialog>`
    )
    setTimeout(() => {
        $('body dialog').remove()
    }, 2000)
}

// function message_box(message, id, url_name) {
//   // Append the message box to the body
//   $('body').append(
//     `<style>
//       .message_box-container {
//         position: fixed;
//         top: 0;
//         left: 0;
//         width: 100%;
//         height: 100%;
//         display: flex;
//         align-items: center;
//         justify-content: center;
//         padding: 1rem;
//         z-index: 100;
//         background: rgba(0, 0, 0, 0.5); /* Semi-transparent background to create a blur effect */
//       }

//       .message_box {
//         height: auto;
//         width: 0vw;
//         border-radius: 5px;
//         border: 1px solid #000;
//         font-size: 18px;
//         text-align: center;
//         background: #f7f4f4;
//         overflow: hidden;
//       }
//     </style>
//     <div class="message_box-container" onclick="noButton()">
//       <dialog id="message_box" class="message_box" open>
//         ${message}<br>
//         <button type="button" class="btn-add-edit" onclick="yesButton('${url_name}', ${id})">Yes</button>
//         <button type="button" class="btn-add-edit" onclick="noButton()" id="noButton">No</button>
//       </dialog>
//     </div>`
//   );

//   var noButton = document.getElementById('noButton');
//   noButton.focus();
// }

function message_box(message, url_name, id) {
  // Append the message box to the body
  $('body').append(
    `<style>
      .message_box-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        z-index: 100;
        background: rgba(0, 0, 0, 0.5); /* Semi-transparent background to create a blur effect */
      }

      .message_box {
        height: auto;
        width: 40vw;
        border-radius: 5px;
        border: 1px solid #000;
        font-size: 18px;
        text-align: center;
        background: #f7f4f4;
        overflow: hidden;
      }
    </style>
    <div class="message_box-container" onclick="noButton()">
      <dialog id="message_box" class="message_box" open>
        ${message}<br>
        <button type="button" class="btn-add-edit" onclick="yesButton('${url_name}', '${id}')" id="yesButton">Yes</button>
        <button type="button" class="btn-add-edit" onclick="noButton()" id="noButton">No</button>
      </dialog>
    </div>`
  );

  var noButton = document.getElementById('noButton');
  noButton.focus();
}

const yesButton = (url_name, id) => {
  window.location.href = `/${url_name}${(id) ? '/' + id : NaN}`;
}

function noButton() {
  // Remove the message box container
  $('.message_box-container').remove();
}

// document.addEventListener('focus', function (event) {
//   var modal = document.getElementById('modal');  
//   if (event.target == modal) {
//     var noButton = document.getElementById('No-delete');
//   noButton.focus();
//   }
// });

// document.addEventListener('click', function (event) {
//   var modal = document.getElementById('modal');
//   var focusedElement = document.getElementById('No-delete');
//   if (event.target === modal &&  modal.hasAttribute('open')) {
//     focusedElement.click();
//   }
// });
// const date_to_yyyymmdd = (date_id) => {
//   const originalDate = $(date_id).val();

//   // Create a Date object from the original date
//   const dateObject = new Date(originalDate);

//   // Get the year, month, and day from the Date object
//   const year = dateObject.getFullYear();
//   const month = String(dateObject.getMonth() + 1).padStart(2, '0'); // Months are zero-based
//   const day = String(dateObject.getDate()).padStart(2, '0');

//   // Create the formatted date in yyyy-mm-dd format
//   const formattedDate = `${year}-${month}-${day}`;
//   console.log(formattedDate);
//   return formattedDate;
// }

// const does_field_exist = (tbl_name, tbl_field, field_value, callback) => {
//   const value = $(field_value).val() || 0;
//   $.ajax({
//     url: `/does_field_exist/${tbl_name}/${tbl_field}/${value}`,  // Correct URL structure
//     method: 'GET',
//     success: function(response) {
//       if (response.result) {
//         // If the field exists, execute the callback with true
//         callback(true);
//       } else {
//         // If the field doesn't exist, execute the callback with false
//         callback(false);
//       }
//     },
//     error: function() {
//       // If there's an error, execute the callback with false
//       callback(false);
//     }
//   });
// };

// const restrict_2_decimal = () => {
//   let inputValue = $(this).text().trim();

//     // Remove any non-numeric characters except for a dot (.)
//     inputValue = inputValue.replace(/[^0-9.]/g, '');

//     // Split the value into integer and decimal parts
//     const parts = inputValue.split('.');

//     // Keep up to 2 decimal places
//     if (parts.length > 1) {
//         inputValue = parts[0] + '.' + parts[1].slice(0, 2);
//     }

//     // Update the input value
//     $(this).text(inputValue);
// }

// $(document).ready(function () {
//     const inputElement = $('#productSearch');
//     const suggestionsElement = $('#suggestions');

//     inputElement.on('input', function () {
//         const query = inputElement.val();
//         if (query) {
//             $.get('/autocomplete', { query: query }, function (data) {
//                 // Clear previous suggestions
//                 suggestionsElement.empty();
                
//                 // Add new suggestions
//                 $.each(data, function (index, suggestion) {
//                     suggestionsElement.append(`<div>${suggestion}</div>`);
//                 });
//             });
//         } else {
//             // Clear suggestions when the input is empty
//             suggestionsElement.empty();
//         }
//     });
// });


// $(document).ready(function () {
//     const inputElement = $('#productSearch');
//     const suggestionsElement = $('#suggestions');
//     let selectedSuggestionIndex = -1;  // Initialize with -1 (no suggestion selected)

//     inputElement.on('input', function () {
//         const query = inputElement.val();
//         if (query) {
//             $.get('/autocomplete', { query: query }, function (data) {
//                 // Clear previous suggestions
//                 suggestionsElement.empty();

//                 // Add new suggestions
//                 $.each(data, function (index, suggestion) {
//                     // Create a suggestion element and attach a click event
//                     const suggestionElement = $('<div>').text(suggestion);

//                     suggestionElement.on('click', function () {
//                         // Set the input field's value to the clicked suggestion
//                         inputElement.val(suggestion);
//                         // Clear the suggestions
//                         suggestionsElement.empty();
//                     });

//                     // Append the suggestion element to the suggestions container
//                     suggestionsElement.append(suggestionElement);

//                     // Highlight the first suggestion
//                     if (index === 0) {
//                         suggestionElement.addClass('selected');
//                     }
//                 });

//                 // Show the suggestions
//                 suggestionsElement.css('display', 'block');
//             });
//         } else {
//             // Clear suggestions and hide the suggestions when the input is empty
//             suggestionsElement.empty();
//             suggestionsElement.css('display', 'none');
//         }
//     });

//     inputElement.on('keydown', function (e) {
//         const suggestionElements = suggestionsElement.find('div');

//         if (suggestionElements.length === 0) {
//             return; // No suggestions to navigate
//         }

//         if (e.key === 'ArrowUp') {
//             // Move selection up
//             selectedSuggestionIndex = Math.max(selectedSuggestionIndex - 1, 0);
//         } else if (e.key === 'ArrowDown') {
//             // Move selection down
//             selectedSuggestionIndex = Math.min(selectedSuggestionIndex + 1, suggestionElements.length - 1);
//         }

//         // Remove the 'selected' class from all suggestions
//         suggestionElements.removeClass('selected');

//         // Add the 'selected' class to the currently selected suggestion
//         suggestionElements.eq(selectedSuggestionIndex).addClass('selected');

//         // Set the input field's value to the selected suggestion
//         inputElement.val(suggestionElements.eq(selectedSuggestionIndex).text());
//     });

//     inputElement.on('blur', function () {
//         // Hide suggestions when the input field loses focus
//         suggestionsElement.css('display', 'none');
//     });
// });










// function validateForm() {
//   // Get the selected value of the "unit" select element
//   var unitSelect = document.getElementById('unit');
//   var selectedValue = unitSelect.value;

//   // Check if the selected value is "0"
//   if (selectedValue === '0') {
//       // Display an alert or message to inform the user
//       alert('Please select a valid unit.');

//       // Prevent the form from submitting
//       return false;
//   }

//   // If the selected value is not "0," the form will be submitted
//   return true;
// }

// document.getElementById('unit').addEventListener('change', function() {
//     var unit = document.getElementById('unit');
//     var label = document.querySelector('.floating-label-select');
    
//     if (unit.value === '0') {
//         label.style.top = '0';
//     } else {
//         label.style.top = '7px';
//     }
// });

// var enableElements = false;
// function productAdd() {
//   const formElements = document.querySelectorAll("input, select, textarea");
//   const btn = document.getElementById("product__btn-submit");
//   const btn_cancel = document.getElementById("product__btn-cancel");

//   if (enableElements) {
//     // At least one element was enabled, reload the page
//     location.reload();
//   }
//   for (const element of formElements) {
//     if (element.classList.contains("disabled-input")) {
//       // Element is currently disabled, so enable it
//       element.classList.remove("disabled-input");

//       if (element.tagName === "SELECT") {
//         element.selectedIndex = 0;
//       } else if (element.type === "text" || element.tagName === "TEXTAREA" || element.type === "number") {
//         element.value = "";
//       }
      
//       enableElements = true; // At least one element was enabled
//     }
//   }
  

//   // Toggle the display of the button
//   btn.style.display = btn_cancel.style.display = btn.style.display === "none" ? "block" : "none";
// }

// const searchInput = document.getElementById("productSearch");

// import { get } from 'axios';

// searchInput.addEventListener("input", (event) => {
//     const searchQuery = event.target.value.toLowerCase();
    
//     // Make an AJAX request to the search_products view
//     get('/product_json/?search_query=${searchQuery}', {
//         params: {
//             search_query: searchQuery
//         }
//     })
//     .then(response => {
//         const filteredProducts = response.data.products;
//         updateTable(filteredProducts);
//     })
//     .catch(error => {
//         console.error('Error fetching data:', error);
//     });
// });

// function updateTable(filteredProducts) {
// const tableBody = document.querySelector("tbody");
// tableBody.innerHTML = "";
// filteredProducts.forEach((product) => {
//     const row = document.createElement("tr");
//     row.innerHTML = `
//     <th class="py-2"><p class="text-black font-semibold text-base">${product.id}</p></th>
//     <th class="py-2"><a href="{% url 'product' product.id %}"><p class="text-black font-semibold text-base">${product.product_code}</p></a></th>
//     <th class="py-2"><a href="{% url 'product' product.id %}"><p class="text-black font-semibold text-base product-name">${product.product_name}</p></a></th>
//     <th class="py-2"><p class="text-black font-semibold text-base">${product.price}</p></th>
//     <th class="py-2"><p class="text-black font-semibold text-base">${product.stock}</p></th>
//     <th class="py-2"><p class="text-black font-semibold text-base">${product.vendor}</p></th>
//     <th class="py-2"><p class="text-black font-semibold text-base">${product.category}</p></th>
//     `;
//     tableBody.appendChild(row);
//     });
// }