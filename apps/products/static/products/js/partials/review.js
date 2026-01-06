document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll(".clickable-star");
    const ratingInput = document.getElementById("rating-input");
    const form = document.querySelector(".product-reviews form");

    stars.forEach((star) => {
        star.addEventListener("click", function() {
            const val = parseInt(this.getAttribute("data-value"));
            updateStars(val);
            if (ratingInput) {
                ratingInput.value = val;
            }
        });
    });

    function updateStars(val) {
        stars.forEach((star) => {
            const starVal = parseInt(star.getAttribute("data-value"));
            // Troca o ícone dependendo da nota selecionada
            star.src = starVal <= val
                ? "/static/products/media/icons/star-filled.svg"
                : "/static/products/media/icons/star.svg";
        });
    }

    if (form) {
        form.addEventListener("submit", (e) => {
            if (!ratingInput.value || ratingInput.value === "0") {
                e.preventDefault();
                alert("Por favor, selecione uma nota clicando nas estrelas.");
            }
        });
    }
});