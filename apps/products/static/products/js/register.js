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

document.getElementById('productForm').addEventListener('submit', function (e) {
  const variantsArray = [];

  // 1. Percorrer cada card de variante
  document.querySelectorAll('.variant-card').forEach(card => {
    
   const attributes = [];

// Pegamos todas as linhas de atributo do card
card.querySelectorAll('.attribute-row').forEach(row => {
    
    // Em vez de classe, buscamos diretamente pela tag que o Django gerou
    const selectEl = row.querySelector('select'); // O campo 'attribute'
    const inputEl = row.querySelector('input[type="text"]'); // O campo 'value'

    if (selectEl && inputEl) {
        const id = selectEl.value;
        const val = inputEl.value;

        if (id && val) {
            attributes.push({ 
                attribute_id: id, 
                value: val 
            });
        }
    }
});

// TESTE: Mostra no console se pegou algo
console.log("Atributos capturados:", attributes);

    // 3. Capturar os campos da variante (SKU, Preço, etc)
    // Usamos seletores que buscam o final do nome do input gerado pelo Django
    const variantData = {
      sku: card.querySelector('[name$="-sku"]').value,
      price: card.querySelector('[name$="-price"]').value,
      type: card.querySelector('[name$="-type"]').value,
      stock: card.querySelector('[name$="-stock"]')?.value || null,
      production_days: card.querySelector('[name$="-production_days"]')?.value || null,
      is_customizable: card.querySelector('[name$="-is_customizable"]')?.checked || false,
      attributes: attributes // Insere o array de atributos aqui dentro
    };

    variantsArray.push(variantData);
  });

  // 4. Transformar o array completo em string JSON e colocar no input escondido
  document.getElementById('variantsJsonInput').value = JSON.stringify(variantsArray);
  
  // O formulário seguirá o envio normal, levando o product_form e o variants_json
});
(function () {
  const prefix = 'variants'; // garanta que o formset no view use prefix='variants'
  const totalFormsInput = document.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
  const initialFormsInput = document.querySelector(`input[name="${prefix}-INITIAL_FORMS"]`);
  const variantsContainer = document.getElementById('variantsContainer');
  const addVariantBtn = document.getElementById('addVariantButton');
  const emptyTemplateHTML = document.getElementById('emptyVariantTemplate').innerHTML;
  const deletedInput = document.getElementById('deletedVariantsInput');

  // util
  function getTotalForms() { return parseInt(totalFormsInput.value, 10); }
  function setTotalForms(v) { totalFormsInput.value = String(v); }
  function getInitialForms() { return parseInt(initialFormsInput.value, 10); }
  function setInitialForms(v) { initialFormsInput.value = String(v); }

  // cria um novo card a partir do empty_form substituindo __prefix__
  function renderEmptyForm(index) {
    return emptyTemplateHTML
      .replace(/__prefix__/g, index)
      .replace(/__num__/g, (index + 1));
  }

  // adiciona uma nova variante (clona empty_form)
  function addVariant() {
    const index = getTotalForms();
    const wrapper = document.createElement('div');
    wrapper.innerHTML = renderEmptyForm(index);
    const card = wrapper.firstElementChild;
    // marca como "nova" (não inicial)
    card.dataset.initial = 'false';
    card.dataset.index = index;
    variantsContainer.appendChild(card);
    setTotalForms(index + 1);
    // opcional: focar no novo card
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  // adiciona um atributo ao card (clona template)
  function addAttributeToCard(card, attributeId='', value='') {
    const tpl = document.getElementById('attributeTemplate');
    const node = tpl.content.cloneNode(true);
    // preencher valores se fornecidos
    if (attributeId) {
      node.querySelector('.attribute-select').value = attributeId;
    }
    if (value) {
      node.querySelector('.attribute-value').value = value;
    }
    card.querySelector('.attribute-list').appendChild(node);
  }

  // serializa atributos do card para o hidden JSON
  function serializeAttributes(card) {
    const arr = [];
    card.querySelectorAll('.attribute-row').forEach(row => {
      const attr = row.querySelector('[data-attr="attribute"]').value;
      const val = row.querySelector('[data-attr="value"]').value;
      if (attr && val) {
        arr.push({ attribute_id: attr, value: val });
      }
    });
    const hidden = card.querySelector('.variant-attributes-json');
    if (hidden) hidden.value = JSON.stringify(arr);
  }

  // reindexa todos os cards para ficarem 0..N-1 e corrige nomes dos inputs
  function reindexAll() {
    const cards = Array.from(variantsContainer.querySelectorAll('.variant-card'));
    cards.forEach((card, newIndex) => {
      const oldIndex = card.dataset.index;
      card.dataset.index = newIndex;
      // atualiza título
      const title = card.querySelector('h5');
      if (title) title.textContent = `Variante ${newIndex + 1}`;
      // atualizar todos os elementos com attribute name
      card.querySelectorAll('[name]').forEach(el => {
        // substitui o primeiro ocorrência variants-\d+- por variants-newIndex-
        el.name = el.name.replace(new RegExp(`${prefix}-\\d+-`), `${prefix}-${newIndex}-`);
      });
      // também atualiza any id attributes (opcional)
      card.querySelectorAll('[id]').forEach(el => {
        el.id = el.id.replace(new RegExp(`${prefix}-\\d+-`), `${prefix}-${newIndex}-`);
      });
      // atualizar hidden JSON name se existir
      const jsonHidden = card.querySelector('.variant-attributes-json');
      if (jsonHidden) jsonHidden.name = `${prefix}-${newIndex}-attributes`;
    });
    // atualizar TOTAL_FORMS
    setTotalForms(cards.length);
    // ajustar INITIAL_FORMS para quantidade de cards que são iniciais
    const remainingInitials = cards.filter(c => c.dataset.initial === 'true').length;
    setInitialForms(remainingInitials);
  }

  // remover variante:
  // - se for existente (data-initial=true e possui data-variant-id) -> registrar id em deleted_variants
  // - remover card DOM (então reindexar todos)
  function removeVariantCard(card) {
    const variantId = card.dataset.variantId;
    const isInitial = card.dataset.initial === 'true';
    if (isInitial && variantId) {
      // registra para backend remover
      const current = deletedInput.value ? JSON.parse(deletedInput.value) : [];
      current.push(variantId);
      deletedInput.value = JSON.stringify(current);
    }
    // remove o card do DOM (novo ou existente) e reindexa
    card.remove();
    reindexAll();
  }

  // evento delegation
  document.addEventListener('click', function (e) {
    const addAttrBtn = e.target.closest('.add-attribute');
    if (addAttrBtn) {
      const card = addAttrBtn.closest('.variant-card');
      addAttributeToCard(card);
      return;
    }

    const removeAttrBtn = e.target.closest('.remove-attribute');
    if (removeAttrBtn) {
      removeAttrBtn.closest('.attribute-row').remove();
      return;
    }

    const removeVariantBtn = e.target.closest('.remove-variant');
    if (removeVariantBtn) {
      const card = removeVariantBtn.closest('.variant-card');
      // confirmação opcional
      removeVariantCard(card);
      return;
    }
  });

  // adicionar nova variante
  addVariantBtn.addEventListener('click', function () {
    addVariant();
  });

  // antes de submeter: serializa atributos e reindex para garantir names corretos
  document.getElementById('productForm').addEventListener('submit', function (e) {
    // serializar atributos de cada card
    document.querySelectorAll('.variant-card').forEach(card => {
      serializeAttributes(card);
    });
    // reindex (por segurança)
    reindexAll();
    // OK: form será submetido
  });

  // init: marca data-initial/data-variant-id se houver input id no card
  (function initExisting() {
    const cards = Array.from(variantsContainer.querySelectorAll('.variant-card'));
    cards.forEach((card, idx) => {
      // tenta encontrar campo id dentro do card: name = variants-<idx>-id
      const idInput = card.querySelector(`input[name^="${prefix}-"][name$="-id"]`);
      if (idInput && idInput.value) {
        card.dataset.variantId = idInput.value;
        card.dataset.initial = 'true';
      } else {
        card.dataset.initial = 'false';
      }
      // garantir índice coerente
      card.dataset.index = idx;
      // se quiser popular atributos existentes por variante (edição), adicione aqui:
      // const attrsJson = card.dataset.attrs; if (attrsJson) parse e chamar addAttributeToCard(...)
    });
    // garantir TOTAL_FORMS coerente (caso backend renderize diferente)
    setTotalForms(cards.length);
  })();

})();