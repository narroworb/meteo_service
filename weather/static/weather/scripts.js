document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("city-input");
    const suggestions = document.getElementById("suggestions");
    let activeIndex = -1;

    input.addEventListener("input", function () {
        const query = this.value.trim();
        if (query.length < 2) {
            suggestions.style.display = "none";
            return;
        }

        fetch(`/autocomplete/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                suggestions.innerHTML = "";
                activeIndex = -1;

                if (data.results.length === 0) {
                    suggestions.style.display = "none";
                    return;
                }

                data.results.forEach(city => {
                    const li = document.createElement("li");
                    li.textContent = city;
                    li.tabIndex = 0;
                    li.addEventListener("click", () => {
                        input.value = city;
                        suggestions.style.display = "none";
                        input.focus();
                    });
                    suggestions.appendChild(li);
                });
                suggestions.style.display = "block";
            })
            .catch(() => {
                suggestions.style.display = "none";
            });
    });

    input.addEventListener("keydown", function (e) {
        const items = suggestions.querySelectorAll("li");
        if (items.length === 0) return;

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
            }
        } else if (e.key === "Escape") {
            suggestions.style.display = "none";
        }
    });

    document.addEventListener("click", (e) => {
        if (!suggestions.contains(e.target) && e.target !== input) {
            suggestions.style.display = "none";
        }
    });

    function updateActiveItem(items) {
        items.forEach((item, idx) => {
            if (idx === activeIndex) {
                item.classList.add("active");
                item.scrollIntoView({ block: "nearest" });
            } else {
                item.classList.remove("active");
            }
        });
    }


    const canvas = document.getElementById('tempChart');
    if (!canvas) return;

    const datesScript = document.getElementById('dates-data');
    const tempsScript = document.getElementById('temps-data');
    const iconsScript = document.getElementById('icons-data');

    if (!datesScript || !tempsScript || !iconsScript) return;

    const forecastDates = JSON.parse(datesScript.textContent);
    const forecastTemps = JSON.parse(tempsScript.textContent);
    const forecastIcons = JSON.parse(iconsScript.textContent);

    const iconImages = forecastIcons.map(src => {
        const img = new Image();
        img.src = `/static/weather/icons/${src}`;
        img.width = 16;
        img.height = 16;

        return img;
    });

    const ctx = canvas.getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: forecastDates,
            datasets: [{
                label: 'Температура °C',
                data: forecastTemps,
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                fill: true,
                tension: 0.3,
                pointStyle: iconImages,
                pointRadius: 20,
                pointHoverRadius: 24
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    beginAtZero: false,
                    suggestedMin: Math.min(...forecastTemps) - 5,
                    suggestedMax: Math.max(...forecastTemps) + 5
                }
            }
        }
    });
});

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("city-input");

    // Сохраняем город при отправке формы
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", () => {
            const city = input.value.trim();
            if (city) {
                localStorage.setItem("lastCity", city);
            }
        });
    }

});

document.querySelectorAll('.last-city-btn').forEach(button => {
    button.addEventListener('click', () => {
        const cityInput = document.getElementById('city-input');
        cityInput.value = button.textContent;
        cityInput.form.submit();
    });
});
