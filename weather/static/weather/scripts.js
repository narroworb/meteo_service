const input = document.getElementById("city-input");
const suggestions = document.getElementById("suggestions");

let activeIndex = -1;

input.addEventListener("input", function () {
    const query = this.value.trim();

    if (query.length < 2) {
        suggestions.style.display = "none";
        suggestions.innerHTML = "";
        activeIndex = -1;
        return;
    }

    fetch(`/autocomplete/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            suggestions.innerHTML = "";
            if (data.results.length === 0) {
                suggestions.style.display = "none";
                return;
            }
            data.results.forEach((city, index) => {
                const li = document.createElement("li");
                li.textContent = city;
                li.setAttribute("data-index", index);
                li.addEventListener("click", () => {
                    input.value = city;
                    suggestions.style.display = "none";
                    activeIndex = -1;
                });
                suggestions.appendChild(li);
            });
            activeIndex = -1;
            suggestions.style.display = "block";
        })
        .catch(() => {
            suggestions.style.display = "none";
        });
});

// Обработка клавиш вверх/вниз и Enter для навигации по списку
input.addEventListener("keydown", (e) => {
    const items = suggestions.querySelectorAll("li");
    if (suggestions.style.display === "none" || items.length === 0) return;

    if (e.key === "ArrowDown") {
        e.preventDefault();
        activeIndex = (activeIndex + 1) % items.length;
        updateActiveItem(items);
    } else if (e.key === "ArrowUp") {
        e.preventDefault();
        activeIndex = (activeIndex - 1 + items.length) % items.length;
        updateActiveItem(items);
    } else if (e.key === "Enter") {
        if (activeIndex >= 0 && activeIndex < items.length) {
            e.preventDefault();
            input.value = items[activeIndex].textContent;
            suggestions.style.display = "none";
            activeIndex = -1;
        }
    } else if (e.key === "Escape") {
        suggestions.style.display = "none";
        activeIndex = -1;
    }
});

function updateActiveItem(items) {
    items.forEach((item, i) => {
        if (i === activeIndex) {
            item.classList.add("active");
            item.scrollIntoView({ block: "nearest" });
        } else {
            item.classList.remove("active");
        }
    });
}

// Закрываем список при клике вне поля и списка
document.addEventListener("click", (e) => {
    if (!suggestions.contains(e.target) && e.target !== input) {
        suggestions.style.display = "none";
        activeIndex = -1;
    }
});
