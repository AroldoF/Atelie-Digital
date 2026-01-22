document.addEventListener('DOMContentLoaded', function() {
    const paymentOptions = document.querySelectorAll('.shipping-option');
    const creditCardForm = document.querySelector('.credit_card_form');
    
    const cardInputs = creditCardForm.querySelectorAll('input, select');

    function handlePaymentMethod(method) {
        if (method === 'credit') {
            creditCardForm.style.display = 'block';

            cardInputs.forEach(input => input.removeAttribute('disabled'));
        } else {
            creditCardForm.style.display = 'none';
            cardInputs.forEach(input => input.setAttribute('disabled', 'disabled'));
        }
    }

    const selectedOption = document.querySelector('.shipping-option.selected');
    if (selectedOption) {
        handlePaymentMethod(selectedOption.getAttribute('data-method'));
        const radio = selectedOption.querySelector('input[type="radio"]');
        if(radio) radio.checked = true;
    }

    paymentOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Remove a classe 'selected' de todos
            paymentOptions.forEach(opt => {
                opt.classList.remove('selected');
            });
            
            this.classList.add('selected');

            const radioInput = this.querySelector('input[type="radio"]');
            if (radioInput) {
                radioInput.checked = true;
            }

            const paymentMethod = this.getAttribute('data-method');
            handlePaymentMethod(paymentMethod);
        });
    });
});