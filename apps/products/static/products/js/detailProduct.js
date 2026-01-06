document.addEventListener("DOMContentLoaded", () => {

  /* EXIBIÇÃO DA MÉDIA */
  function renderStaticRating() {
    
    const avgElement = document.getElementById("avg-data");
    if (!avgElement) return;

    const averageRating = parseFloat(avgElement.value.replace(',', '.'));
    const staticStars = document.querySelectorAll(".rating-display-only .imgStar");
    
    staticStars.forEach((star, index) => {
      const starLevel = index + 1;
      if (starLevel <= Math.floor(averageRating)) {
        star.src = "/static/products/media/icons/star-filled.svg";
      }
      // Remove a classe de clique para não mostrar o cursor de 'pointer' no topo
      star.classList.remove("clickable-star");
      star.style.cursor = "default";
    });
  }
  renderStaticRating();
  
  /* BARRAS DE CLASSIFICAÇÃO POR ESTRELAS */
function renderRatingBars() {
  const rows = document.querySelectorAll(".rating-row");

  if (!rows.length) return;

  rows.forEach(row => {
    const percentage = parseFloat(row.dataset.percentage) || 0;

    const bar = row.querySelector(".progress-bar");
    const text = row.querySelector(".percentage-text");

    // Aplica largura da barra
    bar.style.width = percentage + "%";

    // Atualiza texto
    text.textContent = Math.round(percentage) + "%";
  });
}

renderRatingBars();



  /* MODAL */
  //  apenas as estrelas que estão dentro da área do modal
  const modalStars = document.querySelectorAll("#modal-rating-area .imgStar");
  const ratingInput = document.getElementById("rating-input");

  if (modalStars.length > 0) {
    modalStars.forEach((star) => {
      star.addEventListener("click", function() {
        const val = parseInt(this.getAttribute("data-value"));
        
        // Atualiza o input hidden para o POST do Django
        if (ratingInput) ratingInput.value = val;

        // "Pinta" as estrelas até o valor clicado
        modalStars.forEach((s) => {
          const starVal = parseInt(s.getAttribute("data-value"));
          s.src = starVal <= val 
            ? "/static/products/media/icons/star-filled.svg" 
            : "/static/products/media/icons/star.svg";
        });
      });
    });
  }


  /* MOBILE CAROUSEL  */
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

    prevBtn.onclick = () => {
      index = (index - 1 + items.length) % items.length;
      updateCarousel();
    };
    nextBtn.onclick = () => {
      index = (index + 1) % items.length;
      updateCarousel();
    };
    function goTo(i) {
      index = i;
      updateCarousel();
    }
  }

  const mobileCarousel = document.querySelector(".mobile-only");
  if (mobileCarousel) {
    initMobileCarousel(mobileCarousel);
  }


  /* DESKTOP GALLERY (Original)*/
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


  /* QUANTIDADE  */
  window.changeQuantity = function (delta) {
    const input = document.getElementById("quantity");
    if (!input) return;

    let value = parseInt(input.value) || 1;
    value += delta;
    value = Math.max(1, Math.min(20, value));
    input.value = value;
  };

});