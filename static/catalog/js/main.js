function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
  const deleteButton = document.getElementById("delete_button");
  const buyButton = document.getElementById("buy_button");

  const currentUrl = window.location.href;

  const csrftoken = getCookie("csrftoken");

  if (deleteButton) {
    deleteButton.addEventListener("click", function () {
      fetch(`${currentUrl}delete/`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": csrftoken,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            console.log("Товар удален");
            window.location.href = document.referrer; // Перенаправление на предыдущую страницу
          }
        })
        .catch((error) => console.error("Ошибка:", error));
    });
  }

  if (buyButton) {
    buyButton.addEventListener("click", function () {
      const productId = this.getAttribute("data-id");
      var url = window.location.origin + "/basket/add/";
      console.log(url);
      console.log(productId);
      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ product_id: productId }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "error") {
            alert("Ошибка при добавлении товара в корзину");
          } else {
            window.location.href = /basket/;
          }
        })
        .catch((error) => console.error("Ошибка:", error));
    });
  }
});
