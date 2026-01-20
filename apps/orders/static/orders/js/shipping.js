document.addEventListener('DOMContentLoaded', function() {
// Selecionar endereço ao clicar no card inteiro
    document.querySelectorAll('.address-card').forEach(card => {
        card.addEventListener('click', function(e) {
        if (e.target !== this.querySelector('input[type="radio"]') && 
            !e.target.classList.contains('address-edit')) {
            this.querySelector('input[type="radio"]').checked = true;
        }
        });
    });

    // Selecionar frete ao clicar no card inteiro
    document.querySelectorAll('.shipping-option').forEach(option => {
        option.addEventListener('click', function(e) {
        if (e.target !== this.querySelector('input[type="radio"]')) {
            this.querySelector('input[type="radio"]').checked = true;
        }
        });
    });
});