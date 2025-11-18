document.addEventListener('DOMContentLoaded', function() {
    const payment_options = document.querySelectorAll('.field-option');
    
    payment_options.forEach(option => {
        option.addEventListener('click', function() {
            payment_options.forEach(opt => {
                opt.classList.remove('selected');
            });
            
            this.classList.add('selected');
 
            const payment_method = this.getAttribute('data-method');
            const credit_card_form = document.querySelector('.credit_card_form'); // Assumindo uma classe para o formulário
            if (payment_method === 'credit') {
                credit_card_form.style.display = 'block';
            } else {
                credit_card_form.style.display = 'none';
            }
        });
    });
});