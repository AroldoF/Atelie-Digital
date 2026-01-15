
document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Encontra TODOS os seletores de quantidade na página
    const quantitySelectors = document.querySelectorAll(".quantity-selector");
    
    // 2. Itera sobre cada um deles
    quantitySelectors.forEach(selector => {
        
        // 3. Encontra os botões e o valor DENTRO de cada seletor
        const decreaseBtn = selector.querySelector("[data-action='decrease']");
        const increaseBtn = selector.querySelector("[data-action='increase']");
        const valueSpan = selector.querySelector(".quantity-value");
        
        // 4. Adiciona o clique no botão de DECREMENTAR
        decreaseBtn.addEventListener("click", () => {
            let currentValue = parseInt(valueSpan.textContent);
            if (currentValue > 1) { // Não deixa ser menor que 1
                valueSpan.textContent = currentValue - 1;
            }
        });
        
        // 5. Adiciona o clique no botão de INCREMENTAR
        increaseBtn.addEventListener("click", () => {
            let currentValue = parseInt(valueSpan.textContent);
            valueSpan.textContent = currentValue + 1;
        });
    });
});