document.addEventListener("DOMContentLoaded", () => {

  /* MOBILE CAROUSEL */
  function initMobileCarousel(container) {
    const items = container.querySelectorAll(".carouselItem");
    const prevBtn = container.querySelector(".carousel-btn.prev");
    const nextBtn = container.querySelector(".carousel-btn.next");
    const dotsContainer = container.querySelector(".carousel-dots");

    if (!items.length || !prevBtn || !nextBtn || !dotsContainer) return;

    const DOT = "/static/products/media/icons/circle.svg";
    const DOT_ACTIVE = "/static/products/media/icons/circleCurrent.svg";
    let index = 0;

    dotsContainer.innerHTML = "";

    items.forEach((_, i) => {
      const dot = document.createElement("img");
      dot.src = i === 0 ? DOT_ACTIVE : DOT;
      dot.dataset.index = i;
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

    prevBtn.onclick = prev;
    nextBtn.onclick = next;
  }

  const mobileCarousel = document.querySelector(".mobile-only");
  if (mobileCarousel) {
    initMobileCarousel(mobileCarousel);
  }

  /*  DESKTOP GALLERY */
  function initDesktopGallery() {
    const mainImageDesktop = document.getElementById("mainImageDesktop");
    const thumbs = document.querySelectorAll(".thumbnail");

    if (!mainImageDesktop || !thumbs.length) return;

    thumbs.forEach((thumb) => {
      thumb.onclick = () => {
        mainImageDesktop.src = thumb.dataset.src;
        thumbs.forEach(t => t.classList.remove("active"));
        thumb.classList.add("active");
      };
    });
  }

  initDesktopGallery();

  /*  QUANTIDADE */
  window.changeQuantity = function (delta) {
    const input = document.getElementById("quantity");
    if (!input) return;

    let value = parseInt(input.value) || 1;
    value += delta;
    value = Math.max(1, Math.min(20, value));
    input.value = value;
  };

});
