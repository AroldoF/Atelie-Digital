
(function () {
  // evita adicionar múltiplos listeners se o arquivo for carregado mais de uma vez
  if (window.__drop_js_initialized) return;
  window.__drop_js_initialized = true;

  // retorna true se o elemento (ou algum pai) estiver invisível de forma prática
  function isEffectivelyHidden(el) {
    if (!el) return true;

    // se elemento (ou algum ancestor) tem display: none, visibility: hidden, opacity: 0 ou aria-hidden="true"
    let node = el;
    while (node && node.nodeType === 1) { 
      const style = window.getComputedStyle(node);

      if (style.display === 'none') return true;
      if (style.visibility === 'hidden') return true;
      if (parseFloat(style.opacity) === 0) return true;
      if (node.hasAttribute && node.getAttribute('aria-hidden') === 'true') return true;

      node = node.parentElement;
    }

    return false;
  }

  function toggleDrop(header) {
    const drop = header.closest('.drop');
    if (!drop) return;

    const icon = header.querySelector('.dropIcon');

    // toggle class
    drop.classList.toggle('open');

    // atualiza ícone com fallback seguro (se icon não existir, ignora)
    if (icon && icon.tagName.toLowerCase() === 'img') {
      icon.src = drop.classList.contains('open')
        ? '/static/products/media/icons/chevron-up.svg'
        : '/static/products/media/icons/chevron-down.svg';
    }
  }

  // Delegação: só responde a clicks com closest('.dropHeader')
  document.addEventListener('click', (event) => {
    const header = event.target.closest('.dropHeader');
    if (!header) return;

    
    if (isEffectivelyHidden(header)) return;


    toggleDrop(header);
  });

 

})();
