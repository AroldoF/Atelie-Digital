document.addEventListener("click", event => {
  const header = event.target.closest(".dropHeader");
  if (!header) return;

  const drop = header.parentElement;
  const icon = header.querySelector(".dropIcon");

  drop.classList.toggle("open");

  icon.src = drop.classList.contains("open")
    ? "/static/products/media/icons/chevron-up.svg"
    : "/static/products/media/icons/chevron-down.svg";
});
