const URL = window.location;

function sendMatrix(data) {
  return fetch(URL, {
    method: 'POST',
    body: data,
  })
    .then(response => {
      if (!response.ok) {
        throw new Error(`Что-то пошло не так: ${response.status}`); 
      }
      return response.status;
    })
}

const matrixForm = document.querySelector("#skills");
const modals = document.querySelector('.modals');
const modalsContent = modals.querySelector('.modals__content');
const modalsCloseButton = modals.querySelector('.modals__button');

matrixForm.addEventListener("submit", (evt) => {
  evt.preventDefault();

  const data = new FormData(matrixForm);

  sendMatrix(data)
  .then(status => {
    if(status === 204) {
      modalsContent.textContent = "Матрицу можно заполнить только один раз в день, Дубина!"
    } else {
      modalsContent.textContent = "Данные успешно сохранены, наверно"
    }

    openModals(modals);

  }).catch(error => console.log(error))
})

function openModals(elem) {
  elem.showModal();
}

function closeModals(elem) {
  elem.close();
}

modalsCloseButton.addEventListener("click", () => {
  closeModals(modals);
  modalsContent.textContent = "";
})