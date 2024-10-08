document.addEventListener("DOMContentLoaded", function () {
  const buttons = document.querySelectorAll(".delete-order");
  buttons.forEach(function (button) {
    button.addEventListener("click", async function () {
      const order_id = this.getAttribute("data-order-id"); // Получаем ID заказа из атрибута data-order-id
      const csrftoken = getCookie("csrftoken"); // Получаем CSRF токен
      const url = window.location.href; // Текущий URL

      try {
        const response = await fetch(url, {
          method: "DELETE",
          headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ order_id: order_id }), // Передаем ID заказа
        });

        if (response.ok) {
          window.location.reload();
        } else {
          alert("Error deleting order: " + response.status);
        }
      } catch (error) {
        console.error("Fetch error: ", error);
        alert("An error occurred while trying to delete the order.");
      }
    });
  });
});

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
