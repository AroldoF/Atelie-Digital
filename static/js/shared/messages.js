var messageContainer = document.querySelector('.message-container');

if (messageContainer) {
    setTimeout(function() {
        messageContainer.classList.add('fade-out');
    }, 2500);

    setTimeout(function() {
        messageContainer.style.display = 'none';
    }, 5000);
}