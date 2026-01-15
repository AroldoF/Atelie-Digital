document.addEventListener("DOMContentLoaded", () => {

  /* --- 1. EXIBIÇÃO DA MÉDIA DE ESTRELAS --- */
  function renderStaticRatings() {
    const avgElement = document.getElementById("avg-data");
    if (!avgElement) return;

    // Substitui vírgula por ponto para garantir float correto
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

          // Bloqueia interação visual
          star.style.pointerEvents = "none";
          star.style.cursor = "default";
        });
      });
  }
  renderStaticRatings();


  /* --- 2. BARRAS DE CLASSIFICAÇÃO (PROGRESS BARS) --- */
  function renderRatingBars() {
    const rows = document.querySelectorAll(".rating-row");
    if (!rows.length) return;

    rows.forEach(row => {
      const percentage = parseFloat(row.dataset.percentage) || 0;
      const bar = row.querySelector(".progress-bar");
      const text = row.querySelector(".percentage-text");

      if (bar && text) {
        bar.style.width = percentage + "%";
        text.textContent = Math.round(percentage) + "%";
      }
    });
  }
  renderRatingBars();


  /* --- 3. ESTRELAS INTERATIVAS DO MODAL --- */
  function initInteractiveStars() {
    const allStars = document.querySelectorAll(".imgStar");
    const ratingInput = document.getElementById("rating-input");

    // Se não tiver input de rating (modal não existe), não faz nada
    if (!ratingInput) return;

    allStars.forEach(star => {
      const isInsideModal = star.closest("#modalAvaliar");

      // Fora do modal -> Bloqueado
      if (!isInsideModal) {
        star.style.pointerEvents = "none";
        star.style.cursor = "default";
        return;
      }

      // Dentro do modal -> Interativo
      star.style.pointerEvents = "auto";
      star.style.cursor = "pointer";

      const value = parseInt(star.dataset.value);

      // Evento Hover
      star.addEventListener("mouseenter", () => {
        highlightStars(value, isInsideModal);
      });

      // Evento Click
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
        () => {
           // Só reseta se o usuário não tiver clicado ainda (input zerado)
           // Ou reseta visualmente para a nota salva
           const ratingInput = document.getElementById("rating-input");
           const savedValue = parseInt(ratingInput.value) || 0;
           
           if(savedValue === 0) {
              resetStars(container);
           } else {
              // Restaura visualmente a nota clicada
              highlightStars(savedValue, container, true);
           }
        },
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


  /* --- 4. MOBILE CAROUSEL --- */
  function initMobileCarousel(container) {
    const items = container.querySelectorAll(".carouselItem");
    const prevBtn = container.querySelector(".carousel-btn.prev");
    const nextBtn = container.querySelector(".carousel-btn.next");
    const dotsContainer = container.querySelector(".carousel-dots");

    if (!items.length || !prevBtn || !nextBtn || !dotsContainer) return;

    const DOT = "/static/products/media/icons/circle.svg";
    const DOT_ACTIVE = "/static/products/media/icons/circleCurrent.svg";
    let index = 0;

    // Gera os dots dinamicamente
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

    prevBtn.onclick = (e) => {
      e.preventDefault(); // Evita scroll ou submit acidental
      goTo((index - 1 + items.length) % items.length);
    }
    
    nextBtn.onclick = (e) => {
      e.preventDefault();
      goTo((index + 1) % items.length);
    }
  }

  const mobileCarousel = document.querySelector(".mobile-only");
  if (mobileCarousel) initMobileCarousel(mobileCarousel);


  /* --- 5. GALERIA DESKTOP --- */
  function initDesktopGallery() {
    const mainImage = document.getElementById("mainImageDesktop");
    const thumbs = document.querySelectorAll(".thumbnail");

    if (!mainImage || !thumbs.length) return;

    thumbs.forEach(thumb => {
      thumb.onclick = () => {
        // Pega URL da imagem grande via data-src
        const bigSrc = thumb.dataset.src || thumb.src;
        mainImage.src = bigSrc;

        // Atualiza classe active
        thumbs.forEach(t => t.classList.remove("active"));
        thumb.classList.add("active");
      };
    });
  }
  initDesktopGallery();

});


/* --- 6. CONTROLE DE QUANTIDADE (GLOBAL) --- */
window.changeQuantity = function (delta) {
  const input = document.getElementById("quantity");
  if (!input) return;

  const min = parseInt(input.min) || 1;
  
  // Pega o max definido no HTML (vem do backend)
  // Se não tiver max (produto sob encomenda), define Infinito
  const maxAttr = input.getAttribute("max");
  const max = maxAttr ? parseInt(maxAttr) : Infinity;

  let currentValue = parseInt(input.value) || min;
  const nextValue = currentValue + delta;

  // Validação simples: só atualiza se estiver dentro dos limites
  if (nextValue >= min && nextValue <= max) {
    input.value = nextValue;
  } 
  
};