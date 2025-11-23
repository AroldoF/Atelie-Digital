document.addEventListener("DOMContentLoaded", () => {

  // mobile carousel
  const mobileCarousel = document.querySelector(".mobile-only");

  if (mobileCarousel) {
    const items = mobileCarousel.querySelectorAll(".carouselItem");
    const prevBtn = mobileCarousel.querySelector(".carousel-btn.prev");
    const nextBtn = mobileCarousel.querySelector(".carousel-btn.next");
    const dotsContainer = mobileCarousel.querySelector(".carousel-dots");

    // Inicializa somente se TUDO estiver presente
    if (items.length > 0 && prevBtn && nextBtn && dotsContainer) {
      const DOT = "/static/products/media/icons/circle.svg";
      const DOT_ACTIVE = "/static/products/media/icons/circleCurrent.svg";
      let index = 0;

      // Criar dots
      items.forEach((_, i) => {
        const dot = document.createElement("img");
        dot.src = i === 0 ? DOT_ACTIVE : DOT;
        dot.dataset.index = i;
        dot.alt = `Imagem ${i + 1}`;
        dot.style.cursor = "pointer";
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

      prevBtn.addEventListener("click", prev);
      nextBtn.addEventListener("click", next);
      dots.forEach(dot => dot.addEventListener("click", () => goTo(+dot.dataset.index)));
    }
  }

  // desktop gallery
  const desktopThumbs = document.querySelectorAll(".thumbnail");
  const mainImageDesktop = document.getElementById("mainImageDesktop");

  if (desktopThumbs.length > 0 && mainImageDesktop) {
    desktopThumbs.forEach((thumb) => {
      thumb.addEventListener("click", function () {
        const src = this.dataset.src;
        if (src) {
          mainImageDesktop.src = src;
        }
        desktopThumbs.forEach((t) => t.classList.remove("active"));
        this.classList.add("active");
      });
    });
  }

  // função para quantidade
  window.changeQuantity = function (delta) {
    const input = document.getElementById("quantity");
    if (!input) return;

    let value = parseInt(input.value) || 1;
    value += delta;
    value = Math.max(1, Math.min(20, value)); // limite: 1–20
    input.value = value;
  };
});