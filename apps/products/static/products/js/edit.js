/* ==========================================================================
   PRODUTO – JS FINAL (Variantes + Atributos + Imagens + Reindexação Total)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const variantsContainer = document.getElementById('variantsContainer');
    const totalVariantsInput = document.querySelector('input[name="variants-TOTAL_FORMS"]');
    const variantTemplate = document.getElementById('emptyVariantTemplate').innerHTML;
    const attributeTemplate = document.getElementById('attributeTemplate').innerHTML;
    const imageTemplate = document.getElementById('imageTemplate').innerHTML;

    /* --- 1. REINDEXAÇÃO DINÂMICA --- */
    function reindexNestedItems(card, containerSelector, prefixPart) {
    const container = card.querySelector(containerSelector);
    if (!container) return;

    const selector = prefixPart === 'attributes' ? '.attribute-row' : '.image-item-container';
    // MANTER TODOS os itens, inclusive os marcados para exclusão
    const items = Array.from(container.querySelectorAll(selector));
    
    const vIndex = card.dataset.index;

    items.forEach((item, index) => {
        // Regex simples e segura para substituição de prefixos
        const oldPrefixRegex = new RegExp(`variants-\\d+-${prefixPart}-\\d+-`, 'g');
        const newPrefix = `variants-${vIndex}-${prefixPart}-${index}-`;

        item.querySelectorAll('input, select, textarea, label').forEach(el => {
            // PRESERVAR VALORES CRÍTICOS ANTES DE QUALQUER ALTERAÇÃO
            const isHiddenField = el.type === 'hidden';
            const isIdField = el.name && (el.name.includes('-id') || el.name.includes('product'));
            const isDeleteField = el.name && el.name.includes('-DELETE');
            const originalValue = el.value;
            const originalChecked = el.checked;
            
            // ATUALIZAR NAMES E IDS
            if (el.name) {
                el.name = el.name.replace(oldPrefixRegex, newPrefix);
                
                // RESTAURAR VALORES QUE NUNCA DEVEM MUDAR
                if ((isHiddenField && isIdField) || el.name.includes('product')) {
                    el.value = originalValue;
                }
                if (isDeleteField) {
                    el.checked = originalChecked;
                }
            }
            
            if (el.id) {
                el.id = el.id.replace(oldPrefixRegex, newPrefix);
            }
            
            if (el.htmlFor || el.getAttribute('for')) {
                const htmlFor = el.htmlFor || el.getAttribute('for');
                if (htmlFor) {
                    el.htmlFor = htmlFor.replace(oldPrefixRegex, newPrefix);
                    el.setAttribute('for', htmlFor.replace(oldPrefixRegex, newPrefix));
                }
            }
        });
    });

    // Atualizar TOTAL_FORMS com TODOS os formulários
    const totalFormsInput = card.querySelector(`input[name$="-${prefixPart}-TOTAL_FORMS"]`);
    if (totalFormsInput) {
        totalFormsInput.value = items.length;
    }

    // Atualizar INITIAL_FORMS para registros existentes
    const initialFormsInput = card.querySelector(`input[name$="-${prefixPart}-INITIAL_FORMS"]`);
    if (initialFormsInput) {
        // Contar apenas itens que têm ID (registros existentes no banco)
        const existingItems = items.filter(item => {
            const idInput = item.querySelector('input[name$="-id"]');
            return idInput && idInput.value;
        });
        initialFormsInput.value = existingItems.length;
    }
}

function reindexVariants() {
    // MANTER TODAS as variantes (inclusive as marcadas para exclusão)
    const cards = Array.from(variantsContainer.querySelectorAll('.variant-card'));
    
    cards.forEach((card, index) => {
        // Atualizar título e índice
        const title = card.querySelector('h5');
        if (title) title.textContent = `Variante ${index + 1}`;
        card.dataset.index = index;

        // Regex para substituição de prefixos do nível pai
        const oldParentRegex = /variants-\d+-/g;
        const newParentPrefix = `variants-${index}-`;

        card.querySelectorAll('input, select, textarea, label').forEach(el => {
            // PRESERVAR VALORES CRÍTICOS
            const isHiddenField = el.type === 'hidden';
            const isIdField = el.name && (el.name.includes('-id') || el.name.includes('product'));
            const isDeleteField = el.name && el.name.includes('-DELETE');
            const originalValue = el.value;
            const originalChecked = el.checked;
            
            // ATUALIZAR NAMES E IDS
            if (el.name) {
                el.name = el.name.replace(oldParentRegex, newParentPrefix);
                
                // RESTAURAR VALORES ESSENCIAIS QUE NUNCA DEVEM MUDAR
                if ((isHiddenField && isIdField) || 
                    el.name.includes('product') || 
                    el.name.includes('product_variant_id')) {
                    el.value = originalValue;
                }
                if (isDeleteField) {
                    el.checked = originalChecked;
                }
            }
            
            if (el.id) {
                el.id = el.id.replace(oldParentRegex, newParentPrefix);
            }
            
            if (el.htmlFor || el.getAttribute('for')) {
                const htmlFor = el.htmlFor || el.getAttribute('for');
                if (htmlFor) {
                    el.htmlFor = htmlFor.replace(oldParentRegex, newParentPrefix);
                    el.setAttribute('for', htmlFor.replace(oldParentRegex, newParentPrefix));
                }
            }
        });

        // Reindexar formsets aninhados
        reindexNestedItems(card, '.attribute-list', 'attributes');
        reindexNestedItems(card, '.image-list', 'nested_images');
    });

    // Atualizar contadores do formset principal
    if (totalVariantsInput) {
        totalVariantsInput.value = cards.length;
    }
    
    const initialVariantsInput = document.querySelector('input[name="variants-INITIAL_FORMS"]');
    if (initialVariantsInput) {
        // Contar variantes que têm ID (registros existentes)
        const existingVariants = cards.filter(card => {
            const idInput = card.querySelector('input[name$="-id"]');
            return idInput && idInput.value;
        });
        initialVariantsInput.value = existingVariants.length;
    }
}

    function handleImagePreview(input) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            const previewBox = input.closest('.upload-box');
            const previewDiv = previewBox.querySelector('.image-preview');

            reader.onload = (e) => {
                // Limpa apenas os nós de texto dentro da div
                Array.from(previewDiv.childNodes).forEach(node => {
                    if (node.nodeType === Node.TEXT_NODE || node.tagName === "A") {
                        node.remove();
                    }
                });

                // Remove qualquer imagem antiga
                const oldImg = previewDiv.querySelector('img.img-preview-render');
                if (oldImg) oldImg.remove();
                const svgIcon = previewDiv.querySelector('svg');
                if (svgIcon) svgIcon.remove();

                // Cria a nova imagem
                const img = document.createElement('img');
                img.className = 'img-preview-render';
                img.style = "width:135px; height:135px; object-fit:cover; border-radius:8px; padding:5px 5px;";
                img.src = e.target.result;

                previewDiv.appendChild(img);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }


    /* --- 3. VISIBILIDADE DINÂMICA --- */
    function updateVisibility(card) {
        if (!card) return;
        const typeChecked = card.querySelector('input[name$="-type"]:checked')?.value;
        const daysWrap = card.querySelector('[name$="-production_days"]')?.closest('.mb-2');
        const stockWrap = card.querySelector('[name$="-stock"]')?.closest('.mb-2');
        const customWrap = card.querySelector('[name$="-is_customizable"]')?.closest('.mb-2');

        const toggle = (el, show) => { if(el) el.style.display = show ? '' : 'none'; };

        toggle(daysWrap, typeChecked === 'DEMAND');
        toggle(customWrap, typeChecked === 'DEMAND');
        toggle(stockWrap, typeChecked === 'STOCK');
    }

    document.getElementById('addVariantButton').addEventListener('click', () => {
        const index = parseInt(totalVariantsInput.value);
        const newHtml = variantTemplate
            .replace(/__prefix__/g, index)
            .replace(/__num__/g, index + 1);

        variantsContainer.insertAdjacentHTML('beforeend', newHtml);
        totalVariantsInput.value = index + 1;
        updateVisibility(variantsContainer.lastElementChild);
    });

    variantsContainer.addEventListener('click', (e) => {
        const target = e.target;
        const card = target.closest('.variant-card');
        if (!card) return;

        // ADICIONAR ATRIBUTO
        if (target.classList.contains('add-attribute')) {
            const container = card.querySelector('.attribute-list');
            const totalAttrs = card.querySelector(`input[name="variants-${card.dataset.index}-attributes-TOTAL_FORMS"]`);
            const aIndex = parseInt(totalAttrs.value);
            
            let html = attributeTemplate
                .replace(/variants-__prefix__/g, `variants-${card.dataset.index}`)
                .replace(/attributes-__prefix__/g, `attributes-${aIndex}`)
                .replace(/__prefix__/g, aIndex);

            container.insertAdjacentHTML('beforeend', html);
            totalAttrs.value = aIndex + 1;
        }

        // ADICIONAR IMAGEM
        if (target.closest('.addImage')) {
            const container = card.querySelector('.image-list');
            const totalImgs = card.querySelector(`input[name="variants-${card.dataset.index}-images-TOTAL_FORMS"]`);
            const iIndex = parseInt(totalImgs.value);
            const addBtn = target.closest('.addImage');

            let html = imageTemplate
                .replace(/variants-__prefix__/g, `variants-${card.dataset.index}`)
                .replace(/images-__prefix__/g, `images-${iIndex}`)
                .replace(/__prefix__/g, iIndex);

            addBtn.insertAdjacentHTML('beforebegin', html);
            totalImgs.value = iIndex + 1;
        }

        // REMOVER ATRIBUTO
        if (target.classList.contains('remove-attribute')) {
            const row = target.closest('.attribute-row');
            const idInput = row.querySelector('input');

            const deleteInput = row.querySelector('input[name$="DELETE"]');
            
            if (idInput && deleteInput) {
                deleteInput.value = 'on';
                deleteInput.checked = true;
                row.style.display = 'none';

            } else {
                row.remove();
            }
            reindexNestedItems(card, '.attribute-list', 'attributes');
        }

        // REMOVER IMAGEM DA VARIANTE
        if (target.classList.contains('remove-image-btn')) {
            const box = target.closest('.image-item-container');
            const idInput = box.querySelector('input');
            const deleteInput = box.querySelector('input[name$="-DELETE"]');
            if (idInput && idInput.value && deleteInput) {
                deleteInput.value = 'on';
                box.style.display = 'none';
                box.classList.add('is-deleted');
                deleteInput.checked = true;

            } else {
                box.remove();
            }
            reindexNestedItems(card, '.image-list', 'images');
        }

        // REMOVER VARIANTE
        if (target.classList.contains('remove-variant')) {
            const idInput = card.querySelector('input');
            const deleteInput = card.querySelector('input[name$="-DELETE"]');

            if (idInput && idInput.value && deleteInput) {
                deleteInput.value = 'on';
                card.style.display = 'none';
                card.classList.add('is-deleted');
                deleteInput.checked = true;

            
            } else {
                card.remove();
                reindexVariants();
            }
        }

    });

    const mainImageInput = document.getElementById('id_product-image');

    if (mainImageInput) {
        mainImageInput.addEventListener('change', function() {
            handleImagePreview(this);
        });
    }

    /* --- 5. EVENTOS DE MUDANÇA --- */
    variantsContainer.addEventListener('change', (e) => {
        if (e.target.type === 'file') handleImagePreview(e.target);
        if (e.target.name.endsWith('-type')) updateVisibility(e.target.closest('.variant-card'));
    });

    // Inicializa campos existentes no carregamento
    document.querySelectorAll('.variant-card').forEach(updateVisibility);
});

/* --- FUNÇÃO DE REMOÇÃO DE IMAGENS - NÃO UTILIZADA (MANTIDA PARA REFERÊNCIA) --- */
function removeImage(button) {
    // Esta função foi substituída pela lógica no event listener acima
    // Mantida apenas como referência
    const imageLabel = button.closest('.label-image');
    if (!imageLabel) return;

    const card = imageLabel.closest('.variant-card');
    const container = imageLabel.closest('.image-list');
    const idInput = imageLabel.querySelector('input[name$="-id"]');
    const deleteInput = imageLabel.querySelector('input[type="checkbox"][name$="-DELETE"]');

    // 1. Lógica de remoção
    if (idInput && idInput.value) {
        if (deleteInput) deleteInput.checked = true;
        imageLabel.style.display = 'none';
        imageLabel.classList.add('is-deleted');
    } else {
        imageLabel.remove();
    }

    // 2. Reindexação
    if (card && container) {
        reindexNestedItems(card, '.image-list', 'images');
    }
}