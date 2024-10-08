function toggleModal(modalId, show) {
  const modal = document.getElementById(modalId);
  modal.style.display = show ? "flex" : "none";
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie) {
    const cookies = document.cookie.split(";").map((c) => c.trim());
    cookieValue = cookies
      .find((cookie) => cookie.startsWith(name + "="))
      ?.split("=")[1];
    return cookieValue ? decodeURIComponent(cookieValue) : null;
  }
  return null;
}

function sendRequest(url, data) {
  const csrf = getCookie("csrftoken");
  return fetch(url, {
    method: "PUT",
    headers: { "X-CSRFTOKEN": csrf, "Content-Type": "application/json" },
    body: JSON.stringify(data),
  }).then((response) => response.json());
}

document.addEventListener("DOMContentLoaded", () => {
  const url = window.location.href;

  document
    .getElementById("editButton")
    .addEventListener("click", () => toggleModal("modal", true));
  document
    .getElementById("editButtonpassword")
    .addEventListener("click", () => toggleModal("modal-password", true));
  document
    .getElementById("cancelButton")
    .addEventListener("click", () => toggleModal("modal", false));
  document
    .getElementById("cancelButtonpassword")
    .addEventListener("click", () => toggleModal("modal-password", false));

  document.getElementById("confirmButton").addEventListener("click", () => {
    const data = {
      name: document.getElementById("name").value,
      new_email: document.getElementById("email").value,
      phone_number: document.getElementById("phone_number").value,
      telegram_account: document.getElementById("telegram").value,
      salesman: document.getElementById("salesman").checked,
    };
    sendRequest(url, data).then((data) => {
      if (data.status === "success") {
        toggleModal("modal", false);
        location.reload();
      } else {
        document.getElementById("error").innerText = data.error;
      }
    });
  });

  document
    .getElementById("confirmButtonpassword")
    .addEventListener("click", () => {
      const data = {
        old_password: document.getElementById("old_password").value,
        new_password: document.getElementById("new_password").value,
        repeat_password: document.getElementById("repeat_password").value,
      };
      sendRequest(url, data).then((data) => {
        if (data.status === "success") {
          toggleModal("modal-password", false);
        } else {
          document.getElementById("error_password").innerText = data.error;
        }
      });
    });

  document.getElementById("deleteUserButton").addEventListener("click", () => {
    if (confirm("Вы уверены, что хотите удалить пользователя?")) {
      fetch(`${url}`, {
        method: "DELETE",
        headers: { "X-CSRFTOKEN": getCookie("csrftoken") },
      })
        .then((response) => {
          if (response.ok) {
            window.location.href = "/"; // Перенаправляем на главную страницу после удаления
          } else {
            console.error("Ошибка при удалении пользователя");
          }
        })
        .catch(console.error);
    }
  });
});
