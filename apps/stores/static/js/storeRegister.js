document.addEventListener('DOMContentLoaded', function () {
// Máscara adaptativa para telefone (8 ou 9 dígitos)
    const $phone = $('#id_phone_number');
    if ($phone.length) {
        const phoneMaskBehavior = function (val) {
        return val.replace(/\D/g, '').length > 10 ? '(00) 00000-0000' : '(00) 0000-0000';
        };
        const phoneOptions = { onKeyPress: function(val, e, field, options) {
        field.mask(phoneMaskBehavior.apply({}, arguments), options);
        }};
        $phone.mask(phoneMaskBehavior($phone.val()), phoneOptions);
    }

    // Máscara CNPJ
    const $cnpj = $('#id_cnpj');
    if ($cnpj.length) {
        $cnpj.mask('00.000.000/0000-00');
    }

    // --- UPLOAD DE IMAGEM DA LOJA ---
    const imageInput = document.getElementById("id_image");
    const imagePreview = document.getElementById("imagePreview");
    const imagePreviewContainer = document.getElementById("imagePreviewContainer");
    const imageUploadContent = document.getElementById("imageUploadContent");

    if (imageInput && imagePreview) {
        // Preview da imagem
        imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(event) {
            imagePreview.src = event.target.result;
            imagePreviewContainer.style.display = 'flex';
            imageUploadContent.style.display = 'none';
            }
            
            reader.readAsDataURL(file);
        }
        });
    }

    // --- UPLOAD DE BANNER DA LOJA ---
    const bannerInput = document.getElementById("id_banner");
    const bannerPreview = document.getElementById("bannerPreview");
    const bannerPreviewContainer = document.getElementById("bannerPreviewContainer");
    const bannerUploadContent = document.getElementById("bannerUploadContent");

    if (bannerInput && bannerPreview) {
        // Preview do banner
        bannerInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            
            reader.onload = function(event) {
            bannerPreview.src = event.target.result;
            bannerPreviewContainer.style.display = 'flex';
            bannerUploadContent.style.display = 'none';
            }
            
            reader.readAsDataURL(file);
        }
        });
    }

    // --- FEEDBACK VISUAL NO ENVIO ---
    const submitButton = document.querySelector('.btn-submit');
    if (submitButton) {
        submitButton.addEventListener('click', function() {
        const originalText = this.innerHTML;
        this.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
            Processando...
        `;
        this.disabled = true;
        
        // Reverter após 3 segundos (para testes)
        setTimeout(() => {
            this.innerHTML = originalText;
            this.disabled = false;
        }, 3000);
        });
    }
});
