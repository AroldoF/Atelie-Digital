window.addEventListener('load', function() {
    if (window.jQuery) {
        $('#id_cpf').mask('000.000.000-00');
        $('#id_phone_number').mask('(00) 00000-0000');
    }
});


document.addEventListener('DOMContentLoaded', function() {
    
    // Seleciona o campo de input de arquivo pelo ID gerado pelo Django
    // Geralmente é id_ + nome do campo. Ex: id_profile_image
    const fileInput = document.getElementById('id_profile_image'); 
    const imgPreview = document.getElementById('img-preview');

    if (fileInput && imgPreview) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            
            if (file) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    imgPreview.src = e.target.result; // Atualiza a imagem na hora
                }
                
                reader.readAsDataURL(file);
            }
        });
    }
});
