


document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('user');
    console.log(container);
    // Создание экземпляра User и передача ссылки на контейнер
    if (container) {
        new User(container);
    }
}, false);
class User {
    constructor(elem) {
      elem.onclick = this.onClick.bind(this); // (*)
    }

    redirect(url) {
        window.location.href=url
    }
    

      onClick(event) {
        const button = event.target.closest('button'); // Найти ближайший родительский элемент button
        if (button) {
            const url = button.dataset.url;
            this.redirect(url)
        }
    }
  }
