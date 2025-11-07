const conts = document.querySelectorAll(".cont")

let currentCard = 0;
const item = document.querySelectorAll('.card');
const maxItems = item.length;


conts.forEach(control => {
  control.addEventListener('click',(e)=>{
    e.preventDefault();
    const isLeft = control.classList.contains('button-left');
    
 
    if(isLeft){
      currentCard -=1;
    }else{
      currentCard +=1;
    }
    

    if (currentCard >=maxItems){
      currentCard = 0;
    }
    if (currentCard < 0){
      currentCard = maxItems - 1;
    }

    
    item.forEach(item => item.classList.remove('current-card')); 
    
   
    item[currentCard].scrollIntoView({
      inline: "center",
      block: "nearest",  
      behavior: "smooth"
    });
    
   
    item[currentCard].classList.add('current-card'); 
  });
});