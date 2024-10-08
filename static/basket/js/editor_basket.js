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

document.addEventListener("DOMContentLoaded", () => {
  addQuantity();
  removeQuantity();
  document.getElementById("submit").addEventListener("click", editor); // Кнопка "Сохранить изменения"
});

const quantities = {}; // Объект для хранения изменений количества

async function editor() {
  var url = window.location.href;
  const response = await fetch(url, {
    method: "PUT",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"), // Получение CSRF токена
      "Content-Type": "application/json",
    },
    body: JSON.stringify(quantities), // Отправка всех изменений
  });

  if (response.ok) {
    location.reload(); // Перезагрузка страницы для обновления корзины
  } else {
    alert("Ошибка при обновлении количества товара.");
  }
}

function addQuantity() {
  document.querySelectorAll(".increase-quantity").forEach((button) => {
    button.addEventListener("click", function () {
      const itemId = this.getAttribute("data-item-id");
      const quantityElement = document.getElementById(`quantity-${itemId}`);
      let quantity = parseInt(quantityElement.textContent);
      quantityElement.textContent = ++quantity; // Увеличение количества на 1
      quantities[itemId] = quantity; // Обновление объекта с изменениями
    });
  });
}

function removeQuantity() {
  document.querySelectorAll(".decrease-quantity").forEach((button) => {
    button.addEventListener("click", function () {
      const itemId = this.getAttribute("data-item-id");
      const quantityElement = document.getElementById(`quantity-${itemId}`);
      let quantity = parseInt(quantityElement.textContent);
      if (quantity > 1) {
        quantityElement.textContent = --quantity; // Уменьшение количества на 1
        quantities[itemId] = quantity; // Обновление объекта с изменениями
      }
    });
  });
}
