/* ==========================================================================
   PRODUTO – JS FINAL (Django + Crispy + Prefix Safe) - VERSÃO ROBUSTA
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {

  /* ==========================================================================
     1. UPLOAD DE IMAGEM (Preview + Drag & Drop)
     ========================================================================== */
  function initImageUpload() {
    const imageInput = document.querySelector('input[type="file"][name$="image"]');
    const uploadBox = document.getElementById("imageUploadBox");
    const uploadContent = document.getElementById("imageUploadContent");

    if (!imageInput || !uploadBox || !uploadContent) return;

    function preview(file) {
      if (!file) return;
      const reader = new FileReader();
      reader.onload = e => {
        uploadContent.innerHTML = `
          <img src="${e.target.result}" alt="Prévia"
               style="max-height:150px;border-radius:8px;">
          <p class="mt-2 text-muted">Clique ou arraste para trocar a imagem</p>
        `;
      };
      reader.readAsDataURL(file);
    }

    imageInput.addEventListener("change", e => preview(e.target.files[0]));

    ["dragenter", "dragover", "dragleave", "drop"].forEach(ev => {
      uploadBox.addEventListener(ev, e => {
        e.preventDefault();
        e.stopPropagation();
      });
    });

    uploadBox.addEventListener("drop", e => {
      const file = e.dataTransfer.files[0];
      if (!file) return;

      const dt = new DataTransfer();
      dt.items.add(file);
      imageInput.files = dt.files;
      preview(file);
    });
  }

  /* ==========================================================================
     2. VISIBILIDADE DINÂMICA & SELECTORES SEGUROS (DELEGATION)
     - Funciona para todas as variantes (existentes + dinâmicas)
     - Recomendado: template com data-field="..." nos wrappers
     ========================================================================== */

  // helpers genéricos
  function showElement(el) {
    if (!el) return;
    el.style.display = '';
    el.querySelectorAll('input,select,textarea').forEach(i => i.disabled = false);
  }
  function hideElement(el) {
    if (!el) return;
    el.style.display = 'none';
    el.querySelectorAll('input,select,textarea').forEach(i => {
      i.disabled = true;
      i.required = false;
    });
  }

  // determina o escopo (card) a partir de um elemento interno
  function findVariantCard(node) {
    return node.closest ? node.closest('.variant-card') : null;
  }

  // atualiza visibilidade dentro de um card específico
  function updateVisibilityForCard(card) {
  if (!card) return;

  const daysWrap =
    card.querySelector('[data-field="production_days"]')
    || card.querySelector('[name$="production_days"]')?.closest('.mb-2,.mb-3,.form-group');

  const stockWrap =
    card.querySelector('[data-field="stock"]')
    || card.querySelector('[name$="stock"]')?.closest('.mb-2,.mb-3,.form-group');

  const customWrap =
    card.querySelector('[data-field="is_customizable"]')
    || card.querySelector('[name$="is_customizable"]')?.closest('.mb-2,.mb-3,.form-group');

  const checked = card.querySelector(
    'input[type="radio"][name$="type"]:checked'
  );

  /* 🔴 1. SEMPRE ESCONDE TUDO PRIMEIRO */
  hideElement(daysWrap);
  hideElement(stockWrap);
  hideElement(customWrap);

  /* 🟡 2. Se não há tipo escolhido, para aqui */
  if (!checked) return;

  /* 🟢 3. Mostra apenas o permitido */
  if (checked.value === 'DEMAND') {
    showElement(daysWrap);
    showElement(customWrap);
  }

  if (checked.value === 'STOCK') {
    showElement(stockWrap);
  }
}


  // inicializa visibilidade para todos os cards (ou um scope específico)
  function initFieldVisibility(scope = document) {
    const cards = (scope === document)
      ? Array.from(document.querySelectorAll('.variant-card'))
      : (scope.classList && scope.classList.contains('variant-card') ? [scope] : Array.from(scope.querySelectorAll('.variant-card')));
    cards.forEach(updateVisibilityForCard);
  }

  // delegation: qualquer change em radios de type dentro de qualquer card atualiza só o card
  document.addEventListener('change', (e) => {
    // radio change para tipo
    if (e.target.matches('input[type="radio"][name$="type"]') || e.target.matches('[data-field="type"] input[type="radio"]')) {
      const card = findVariantCard(e.target);
      updateVisibilityForCard(card);
    }
  });

  // também expõe função para reinitar quando criar card dinamicamente
  window.reinitVariantUI = function (scope) {
    // scope pode ser um elemento (novo card) ou document
    initFieldVisibility(scope);
    // se precisar: conectar listeners locais adicionais aqui
  };

  /* ==========================================================================
     3. EVENTOS PARA CAMPOS VARIÁVEIS (ex.: price) — delegation para inputs
     - exemplo: captura changes em todos os price inputs mesmo que adicionados depois
     ========================================================================== */

  // escuta qualquer input que tenha name começando com variants- e terminando com -price
  document.addEventListener('input', (e) => {
    // selector por name (formset Django) ou por classe
    if (e.target.matches('[name^="variants-"][name$="-price"]') || e.target.classList.contains('variant-price')) {
      // aqui você faz a ação desejada (validar, recalcular, formatar, etc)
      // ex: console.log('price changed', e.target.name, e.target.value);
      // se precisar do card: const card = findVariantCard(e.target);
    }

    // exemplo genérico: captura alteração em qualquer atributo dinâmico (class usada no form)
    if (e.target.matches('.variant-attr-value') || e.target.matches('[name$="-attributes"]')) {
      // tratamento se você tiver atributos inline
    }
  });

  /* ==========================================================================
     4. INICIALIZAÇÃO E CHAMADAS INICIAIS
     ========================================================================== */
  initImageUpload();
  initFieldVisibility(); // inicializa para os cards gerados pelo Django no GET

  // expõe funções úteis (opcionais)
  window.productUI = {
    initImageUpload,
    initFieldVisibility,
    updateVisibilityForCard,
    findVariantCard
  };
});
