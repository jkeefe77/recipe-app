let filterNameInputField = document.querySelector('#recipe-name-filter')


function filterRecipeNames(val) {
  let tdElements = document.querySelectorAll('.dataframe tbody > tr > td:nth-child(2)')
  tdElements.forEach((td) => {
    if(!td.textContent.toLowerCase().includes(val.toLowerCase())) {
      td.parentElement.classList.add('d-none')
    } else {
      td.parentElement.classList.remove('d-none')
    }
  })
}

filterNameInputField.addEventListener('input', () => filterRecipeNames(filterNameInputField.value))




let filterIngredientsInputField = document.querySelector('#recipe-ingredients-filter')

function filterRecipeIngredients(val) {
  let tdElements = document.querySelectorAll('.dataframe tbody > tr > td:nth-child(5)')
  tdElements.forEach((td) => {
    if(!td.textContent.toLowerCase().includes(val.toLowerCase())) {
      td.parentElement.classList.add('d-none')
    } else {
      td.parentElement.classList.remove('d-none')
    }
  })
}


filterIngredientsInputField.addEventListener('input', () => filterRecipeIngredients(filterIngredientsInputField.value))