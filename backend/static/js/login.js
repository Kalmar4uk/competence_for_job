const URL = "http://localhost:8000/";

const loginForm = document.querySelector(".login-form");
const loginEndpoint = loginForm.action;
const errorMessage = loginForm.querySelector(".login-error");

loginForm.addEventListener("submit", (evt) => {
  evt.preventDefault();

  const data = new FormData(loginForm);

  sendLoginForm(data).then((html) => {
    if (html.querySelector(".login-form")) {
      errorMessage.classList.add("show");
      errorMessage.setAttribute("aria-hidden", "false");
      return;
    }
    errorMessage.classList.remove("show");
    errorMessage.setAttribute("aria-hidden", "true");
    window.location.href = URL;
    return;
  });
});

function sendLoginForm(data) {
  return fetch(loginEndpoint, {
    method: "POST",
    body: data,
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Что-то пошло не так: ${response.status}`);
      }
      return response.text();
    })
    .then((html) => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, "text/html");
      return doc;
    })
    .catch((error) => console.log(error));
}
