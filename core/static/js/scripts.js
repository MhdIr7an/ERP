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