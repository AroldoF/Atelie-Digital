document.addEventListener("DOMContentLoaded", () => {

  /* EXIBIÇÃO DA MÉDIA*/
  function renderStaticRatings() {
  const avgElement = document.getElementById("avg-data");
  if (!avgElement) return;

  const averageRating = parseFloat(avgElement.value.replace(",", ".")) || 0;

  document
    .querySelectorAll('.rating-component[data-mode="display"]')
    .forEach(component => {
      const stars = component.querySelectorAll(".imgStar");

      stars.forEach((star, index) => {
        const level = index + 1;

        star.src =
          level <= Math.floor(averageRating)
            ? "/static/products/media/icons/star-filled.svg"
            : "/static/products/media/icons/star.svg";

        // bloqueia interação
        star.style.pointerEvents = "none";
        star.style.cursor = "default";
      });
    });
}

renderStaticRatings();



  /* BARRAS DE CLASSIFICAÇÃO*/
  function renderRatingBars() {
    const rows = document.querySelectorAll(".rating-row");
    if (!rows.length) return;

    rows.forEach(row => {
      const percentage = parseFloat(row.dataset.percentage) || 0;
      const bar = row.querySelector(".progress-bar");
      const text = row.querySelector(".percentage-text");

      bar.style.width = percentage + "%";
      text.textContent = Math.round(percentage) + "%";
    });
  }
  renderRatingBars();


  /* ESTRELAS INTERATIVAS DO MODAL */
  function initInteractiveStars() {
    const allStars = document.querySelectorAll(".imgStar");
    const ratingInput = document.getElementById("rating-input");

    allStars.forEach(star => {
      const isInsideModal = star.closest("#modalAvaliar");

      // fora do modal  bloqueado
      if (!isInsideModal) {
        star.style.pointerEvents = "none";
        star.style.cursor = "default";
        return;
      }

      // dentro do modal  interativo
      star.style.pointerEvents = "auto";
      star.style.cursor = "pointer";

      const value = parseInt(star.dataset.value);

      // Hover
      star.addEventListener("mouseenter", () => {
        highlightStars(value, isInsideModal);
      });

      // Clique
      star.addEventListener("click", () => {
        ratingInput.value = value;
        highlightStars(value, isInsideModal, true);
      });
    });
  }

  function highlightStars(value, container, persist = false) {
    const stars = container.querySelectorAll(".imgStar");

    stars.forEach(star => {
      const starValue = parseInt(star.dataset.value);
      star.src =
        starValue <= value
          ? "/static/products/media/icons/star-filled.svg"
          : "/static/products/media/icons/star.svg";
    });

    if (!persist) {
      container.addEventListener(
        "mouseleave",
        () => resetStars(container),
        { once: true }
      );
    }
  }

  function resetStars(container) {
    const stars = container.querySelectorAll(".imgStar");
    stars.forEach(star => {
      star.src = "/static/products/media/icons/star.svg";
    });
  }

  initInteractiveStars();


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
      dot.onclick = () => goTo(i);
      dotsContainer.appendChild(dot);
    });

    const dots = dotsContainer.querySelectorAll("img");

    function updateCarousel() {
      items.forEach((item, i) =>
        item.classList.toggle("active", i === index)
      );
      dots.forEach((dot, i) =>
        dot.src = i === index ? DOT_ACTIVE : DOT
      );
    }

    function goTo(i) {
      index = i;
      updateCarousel();
    }

    prevBtn.onclick = () =>
      goTo((index - 1 + items.length) % items.length);
    nextBtn.onclick = () =>
      goTo((index + 1) % items.length);
  }

  const mobileCarousel = document.querySelector(".mobile-only");
  if (mobileCarousel) initMobileCarousel(mobileCarousel);


  /* GALERIA DESKTOP */
  function initDesktopGallery() {
    const mainImage = document.getElementById("mainImageDesktop");
    const thumbs = document.querySelectorAll(".thumbnail");

    if (!mainImage || !thumbs.length) return;

    thumbs.forEach(thumb => {
      thumb.onclick = () => {
        mainImage.src = thumb.dataset.src;
        thumbs.forEach(t => t.classList.remove("active"));
        thumb.classList.add("active");
      };
    });
  }
  initDesktopGallery();
  
  
  
});


// Controle de quantidade do produto baseado no estoque.
window.changeQuantity = function (delta) {
  const input = document.getElementById("quantity");
  const btnPlus = document.getElementById("qty-plus");
  const btnMinus = document.getElementById("qty-minus");

  if (!input) return;

  const min = parseInt(input.min) || 1;
  const maxAttr = input.getAttribute("max");
  const max = maxAttr ? parseInt(maxAttr) : Infinity;

  let value = parseInt(input.value) || min;
  const nextValue = value + delta;

  // Não deixa ultrapassar o estoque
  if (nextValue > max) {
    btnPlus.disabled = true;
    return;
  }

  // Quantidade válida
  btnPlus.disabled = false;
  input.value = Math.max(min, nextValue);

  // Desativa botão − no mínimo
  btnMinus.disabled = input.value <= min;
};


