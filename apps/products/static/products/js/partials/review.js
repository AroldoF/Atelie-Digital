document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll("#review .imgStar");

    stars.forEach((star, index) => {
        star.addEventListener("click", () => {
            updateStars(index);
        });
    });

    function updateStars(activeIndex) {
        stars.forEach((star, i) => {
            if (i <= activeIndex) {
                star.src = "/static/products/media/icons/star-filled.svg";
            } else {
                star.src = "/static/products/media/icons/star.svg";
            }
        });
    }
});
