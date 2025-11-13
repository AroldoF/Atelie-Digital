document.addEventListener("DOMContentLoaded", () => {
  const carousels = document.querySelectorAll('.cardsCarousel');

  carousels.forEach(carousel => {
      const conts = carousel.querySelectorAll(".cont");
      const items = carousel.querySelectorAll('.card');
      const maxItem = items.length;
      let currentCard = 0;

      items.forEach(item => item.classList.remove('current-card')); 
      items[currentCard].scrollIntoView({ inline: "start", block: "nearest", behavior: "auto" });
      items[currentCard].classList.add('current-card'); 

      conts.forEach(control => {
          control.addEventListener('click', (e) => {
              e.preventDefault();
              const isLeft = control.classList.contains('button-left');
              currentCard = isLeft ? currentCard - 1 : currentCard + 1;

              if (currentCard >= maxItem) currentCard = 0;
              if (currentCard < 0) currentCard = maxItem - 1;

              items.forEach(item => item.classList.remove('current-card')); 
              items[currentCard].scrollIntoView({ inline: "start", block: "nearest", behavior: "smooth" });
              items[currentCard].classList.add('current-card'); 
          });
      });
  });
});
