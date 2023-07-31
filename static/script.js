//hide and unhide password feature
function togglePassword(buttonId, passwordId, buttonIconId)
{
    let pass = document.querySelector(`#${passwordId}`);
    if (pass){
        button = document.querySelector(`#${buttonId}`);
        if (button)
        {
            button.addEventListener('click', function(){
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
}

//send base currency selectet value to server to update database and refresh page
function processSelectedItem(selectedValue, destination, divId)
{
    console.log("Selected value:", selectedValue);
    fetch(`/${destination}`,
    {
        method: 'POST',
        headers:
        {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'selected_item': selectedValue }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data);
        let resultDiv = document.getElementById(`${divId}`)
        resultDiv.innerHTML = ` <img src="${data.flag}" class="flag-icon">${data.symbol}`;
    })
    .catch(error => console.error('Error:', error));
}

//goes through list and sends the text of the clicked item to the server
function filterDropdown(optionsListId, destination, divId)
{
    let listItems = document.querySelectorAll(`#${optionsListId} li`);
    if(listItems)
    {
        for (let i = 0; i < listItems.length; i++)
        {
            let listItemAnchor = listItems[i].querySelector('a');
            if (listItemAnchor)
            {
                listItemAnchor.addEventListener('click', function()
                {
                    selectedValue = listItemAnchor.textContent.trim();
                    processSelectedItem(selectedValue, destination, divId)
                });
            }
        }
    }
}

//search box logic for custom dropdown with icons
function implementSearch(searchInputId, listId)
{
    let searchInput = document.querySelector(`#${searchInputId}`);
    let listItems = document.querySelectorAll(`#${listId} li.d-flex`);

    if (searchInput && listItems)
    {
        searchInput.addEventListener('input', function ()
        {
            let searchTerm = searchInput.value.toLowerCase();
            for(let i = 0; i < listItems.length; i++)
            {
                let text = listItems[i].innerText.toLowerCase();
                let isVisible = text.includes(searchTerm);
                if (isVisible)
                {
                    listItems[i].style.setProperty("display", "flex", "important");
                }
                else
                {
                    listItems[i].style.setProperty("display", "none", "important");
                }
            }
        });
    }
}

function searchTable(searchInputId, tableId)
{
    let table = document.querySelectorAll(`#${tableId} tbody tr`);
    let search = document.querySelector(`#${searchInputId}`);
    if (table && search)
    {
        search.addEventListener('input', function()
        {
            let searchTerm = search.value.toUpperCase();
            for (let i = 0; i < table.length; i++)
            {
                let symbolCell = table[i].querySelectorAll('td');
                let symbol = symbolCell[1].textContent.trim();
                let isVisible = symbol.includes(searchTerm);
                if (isVisible)
                {
                    table[i].style.setProperty('display','table-row', 'important');
                }
                else
                {
                    table[i].style.setProperty('display', 'none', 'important');
                }
            }
        })
    }
}


//exchange function
function exchange(inputId, outputId, loseId, checkboxId, yourRateId,destination)
{
    let input = document.querySelector(`#${inputId}`);
    let ose = document.querySelector(`#${loseId}`);
    let output = document.querySelector(`#${outputId}`);
    let check = document.querySelector(`#${checkboxId}`);
    let rate = document.querySelector(`#${yourRateId}`);
    let exact = 0;


    if(input && output && lose && check && rate)
    {
        input.addEventListener('input', function()
        {
            if (isNaN(input.value))
            {
                lose.innerHTML = 'Please input a number';
            }
            else if(input.value)
            {
                fetch(`/${destination}`,
                {
                    method: 'POST',
                    headers:
                    {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 'selected_item': input.value }),
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Response from server:', data);
                    output.placeholder = data.result;
                    exact = data.result;
                    if (check.checked)
                    {
                        if(isNaN(rate.value) || rate.value =="0")
                        {
                            lose.innerHTML = 'Your rate must be a number different from 0.';
                        }
                        else
                        {
                            let result = Number(input.value) * Number(rate.value);
                            console.log(result);
                            let delta = exact - result;
                            if (delta > 0)
                            {
                                lose.innerHTML = `You lose ${delta}.`;
                            }
                            else
                            {
                                lose.innerHTML = `You gain ${-delta}.`;
                            }
                        }
                    }

                })
                .catch(error => console.error('Error'));
            }
            else
            {
                output.placeholder = "";
            }
        });
        rate.addEventListener('input', function()
        {
            if (check.checked)
            {
                if(isNaN(rate.value) || rate.value =="0")
                {
                    lose.innerHTML = 'Your rate must be a number different from 0.';
                }
                else
                {
                    let result = Number(input.value) * Number(rate.value);
                    console.log(result);
                    let delta = exact - result;
                    if (delta > 0)
                    {
                        lose.innerHTML = `You lose ${delta}.`;
                    }
                    else
                    {
                        lose.innerHTML = `You gain ${-delta}.`;
                    }
                }
            }
        });
    }
}

//main script running when page finished loading
document.addEventListener('DOMContentLoaded', function()
{
    togglePassword('show1','password','show_icon1');
    togglePassword('show2','confirm_password','show_icon2');
    togglePassword('show3','current_password','show_icon3');
    implementSearch('dropDownSearch1', 'optionsList1');
    implementSearch('dropDownSearch2', 'optionsList2');
    implementSearch('dropDownSearch3', 'optionsList3');
    filterDropdown('optionsList1','update_base','dropdownMenuButton1');
    filterDropdown('optionsList2','current_base','dropdownMenuButton2');
    filterDropdown('optionsList3','exchange_base','dropdownMenuButton3');
    exchange('amount','exchange_amount','lose','flexCheckDefault','rate','calculate_exchange');
    searchTable('search_table', 'table-rates');
});

