document.addEventListener('DOMContentLoaded', () => {
    const menuButton = document.querySelector('.header__mobile-toggle-button');
    const sidebar = document.getElementById('sidebar-container');

    if (!menuButton || !sidebar) return;

    // Abre/fecha sidebar ao clicar no botão
    menuButton.addEventListener('click', (e) => {
        sidebar.classList.toggle('sidebar--hidden');
        e.stopPropagation(); // evita que o clique "suba" para o document
    });

    // Fecha sidebar se clicar fora dela
    document.addEventListener('click', (e) => {
        // Verifica se o clique não foi dentro da sidebar ou no botão
        if (!sidebar.contains(e.target) && !menuButton.contains(e.target)) {
            sidebar.classList.add('sidebar--hidden');
        }
    });

    // Impede que cliques dentro da sidebar fechem ela
    sidebar.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});