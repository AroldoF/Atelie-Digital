document.addEventListener("DOMContentLoaded", () => {

  const modal = document.getElementById("reviewModal");
  const stars = modal ? modal.querySelectorAll(".clickable-star") : [];
  const ratingInput = document.getElementById("rating-input");
  const form = modal ? modal.querySelector("form") : null;

  if (!stars.length) return;

  stars.forEach(star => {
    star.addEventListener("click", () => {
      const value = parseInt(star.dataset.value);
      ratingInput.value = value;

      stars.forEach(s => {
        s.src = parseInt(s.dataset.value) <= value
          ? "/static/products/media/icons/star-filled.svg"
          : "/static/products/media/icons/star.svg";
      });
    });
  });

  if (form) {
    form.addEventListener("submit", e => {
      if (!ratingInput.value || ratingInput.value === "0") {
        e.preventDefault();
        alert("Por favor, selecione uma nota.");
      }
    });
  }

});
