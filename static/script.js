function togglePassword(buttonId, passwordId, buttonIconId)
{
    let pass = document.querySelector('#' + passwordId);
    if (pass){
        document.querySelector('#' + buttonId).addEventListener('click', function(){
            let button = document.querySelector('#' + buttonIconId);
            if (button.classList.contains('bi-eye-fill'))
            {
                button.classList.remove('bi-eye-fill');
                button.classList.add('bi-eye-slash-fill');
                pass.type = 'text';
            }
            else if (button.classList.contains('bi-eye-slash-fill'))
            {
                button.classList.remove('bi-eye-slash-fill');
                button.classList.add('bi-eye-fill');
                pass.type = 'password';
            }
        });
    }
}

function filterDropdown(dropDownButtonId, optionsListId) {
  let button = document.querySelector('#' + dropDownButtonId);
  let listItems = document.querySelectorAll('#' + optionsListId + ' li');

  if(button && listItems)
  {
    for (let i = 0; i < listItems.length; i++) {
      let imgSrc = listItems[i].querySelector('img');
      let listItemAnchor = listItems[i].querySelector('a');
      if (listItemAnchor && imgSrc){
        listItemAnchor.addEventListener('click', function() {
          button.innerHTML = `<img src="${imgSrc.src}" class="flag-icon">${listItems[i].innerText}`;
          for (let j = 0; j < listItems.length; j++) {
            let anchor = listItems[j].querySelector('a');
            if(anchor){
              anchor.classList.remove('active');
            }
          }
          listItemAnchor.classList.add('active');

          // Send the selected value to the server using AJAX
          let selectedValue = listItemAnchor.textContent.trim();
          console.log("Selected value:", selectedValue);

          fetch('/process_selected_item', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
              },
              body: JSON.stringify({ 'selected_item': selectedValue }),
          })
          .then(response => response.json())
        });
      }
    }
  }
}

function implementSearch(searchInputId, listId) {
  const searchInput = document.querySelector(`#${searchInputId}`);
  const listItems = document.querySelectorAll(`#${listId} li.d-flex`);

  if (searchInput && listItems){
    searchInput.addEventListener("input", function () {
      const searchTerm = searchInput.value.toLowerCase();
      for(let i = 0; i < listItems.length; i++){
        const text = listItems[i].innerText.toLowerCase();
        const isVisible = text.includes(searchTerm);
        if (isVisible){
          listItems[i].style.setProperty("display", "flex", "important");
        }
        else{
          listItems[i].style.setProperty("display", "none", "important");
        }
      }
    });
  }
}


document.addEventListener('DOMContentLoaded', function(){
    togglePassword('show1','password','show_icon1');
    togglePassword('show2','confirm_password','show_icon2');
    togglePassword('show3','current_password','show_icon3');
    filterDropdown('dropdownMenuButton1', 'optionsList');
    implementSearch('dropDownSearch', 'optionsList');
});

