const controls = document.querySelectorAll('.control');

let currentItem = 0;
const items = document.querySelectorAll('.item');
const maxItem = items.length;


controls.forEach(control => {
  control.addEventListener('click',(e)=>{
    e.preventDefault();
    const isLeft = control.classList.contains('arrow-left');
    control.classList.contains("arrow-left");
    if(isLeft){
      currentItem -=1;
    }else{
      currentItem +=1;
    }
    if (currentItem >=maxItem){
      currentItem = 0;
    }
    if (currentItem < 0){
      currentItem = maxItem - 1;
    }

    items.forEach(item => item.classList.remove('current-item'));
    items[currentItem].scrollIntoView({
      inline: "center",
      block: "nearest",  
      behavior: "smooth"
    });
    items[currentItem].classList.add('current-item');
  });
});