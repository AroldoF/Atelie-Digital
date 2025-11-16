document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll(".carouselItem");
    const prevBtn = document.querySelector(".carousel-btn.prev");
    const nextBtn = document.querySelector(".carousel-btn.next");
    const dotsContainer = document.querySelector(".carousel-dots");

    const DOT = "/static/products/media/icons/circle.svg";
    const DOT_ACTIVE = "/static/products/media/icons/circleCurrent.svg";

    let index = 0;

   
    items.forEach((_, i) => {
        const dot = document.createElement("img");
        dot.src = i === 0 ? DOT_ACTIVE : DOT;
        dot.dataset.index = i;

        dot.addEventListener("click", () => goTo(i));

        dotsContainer.appendChild(dot);
    });

    const dots = dotsContainer.querySelectorAll("img");

    function updateCarousel() {
        items.forEach((item, i) => {
            item.classList.toggle("active", i === index);
        });

        dots.forEach((dot, i) => {
            dot.src = i === index ? DOT_ACTIVE : DOT;
        });
    }

    function next() {
        index = (index + 1) % items.length;
        updateCarousel();
    }

    function prev() {
        index = (index - 1 + items.length) % items.length;
        updateCarousel();
    }

    function goTo(i) {
        index = i;
        updateCarousel();
    }

    nextBtn.addEventListener("click", next);
    prevBtn.addEventListener("click", prev);
});
