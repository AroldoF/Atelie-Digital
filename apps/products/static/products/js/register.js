/* ==========================================================================
   PRODUTO – JS FINAL (Variantes + Atributos + Imagens + Reindexação Total)
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    const variantsContainer = document.getElementById('variantsContainer');
    const totalVariantsInput = document.querySelector('input[name="variants-TOTAL_FORMS"]');
    const variantTemplate = document.getElementById('emptyVariantTemplate').innerHTML;
    const attributeTemplate = document.getElementById('attributeTemplate').innerHTML;
    const imageTemplate = document.getElementById('imageTemplate').innerHTML;

    /* --- 1. FUNÇÕES DE REINDEXAÇÃO --- */

    // Reindexa itens internos (Atributos ou Imagens) de uma variante específica
    function reindexNestedItems(card, containerSelector, prefixPart) {
        const container = card.querySelector(containerSelector);
        if (!container) return;

        // Seleciona as linhas de atributos ou os boxes de imagem (exceto o botão de adicionar)
        const selector = prefixPart === 'attributes' ? '.attribute-row' : '.upload-box:not(.addImage)';
        const items = container.querySelectorAll(selector);
        const vIndex = card.dataset.index;

        items.forEach((item, index) => {
            // Regex para encontrar o índice do filho (ex: attributes-2-)
            const regexChild = new RegExp(`${prefixPart}-\\d+-`);
            const newChildPrefix = `${prefixPart}-${index}-`;

            item.querySelectorAll('input, select, textarea, label').forEach(el => {
                if (el.name) el.name = el.name.replace(regexChild, newChildPrefix);
                if (el.id) el.id = el.id.replace(regexChild, newChildPrefix);
                if (el.getAttribute('for')) {
                    el.setAttribute('for', el.getAttribute('for').replace(regexChild, newChildPrefix));
                }
            });
        });

        // Atualiza o TOTAL_FORMS do formset aninhado (Atributos ou Imagens)
        const nestedTotalInput = card.querySelector(`input[name$="-${prefixPart}-TOTAL_FORMS"]`);
        if (nestedTotalInput) {
            nestedTotalInput.value = items.length;
        }
    }

    // Reindexa todas as variantes (O Pai)
    function reindexVariants() {
        const cards = variantsContainer.querySelectorAll('.variant-card');
        
        cards.forEach((card, index) => {
            // 1. Atualiza título e o dataset index
            const title = card.querySelector('h5');
            if (title) title.textContent = `Variante ${index + 1}`;
            card.dataset.index = index;

            // 2. Regex para o prefixo do pai (variants-N-)
            const regexParent = /variants-\d+-/;
            const newParentPrefix = `variants-${index}-`;

            card.querySelectorAll('input, select, textarea, label').forEach(el => {
                if (el.name) el.name = el.name.replace(regexParent, newParentPrefix);
                if (el.id) el.id = el.id.replace(regexParent, newParentPrefix);
                if (el.getAttribute('for')) {
                    el.setAttribute('for', el.getAttribute('for').replace(regexParent, newParentPrefix));
                }
            });

            // 3. Após atualizar o pai, reindexamos os filhos para garantir consistência total
            reindexNestedItems(card, '.attribute-list', 'attributes');
            reindexNestedItems(card, '.image-list', 'images');
        });

        // Atualiza o TOTAL_FORMS principal das variantes
        totalVariantsInput.value = cards.length;
    }

    /* --- 2. PREVIEW DE IMAGENS --- */
    function handleImagePreview(input) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            const previewBox = input.closest('.upload-box');
            const svgIcon = previewBox.querySelector('svg');
            
            reader.onload = (e) => {
                let img = previewBox.querySelector('.img-preview-render');
                if (!img) {
                    img = document.createElement('img');
                    img.className = 'img-preview-render';
                    img.style = "width:135px; height:135px; object-fit:cover; border-radius:8px;";
                    previewBox.appendChild(img);
                }
                img.src = e.target.result;
                if (svgIcon) svgIcon.style.display = 'none';
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

    /* --- 4. GESTÃO DE EVENTOS (Delegation) --- */
    
    // Adicionar Variante
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
            const totalAttrs = card.querySelector('input[name$="-attributes-TOTAL_FORMS"]');
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
            const totalImgs = card.querySelector('input[name$="-images-TOTAL_FORMS"]');
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
            const idInput = row.querySelector('input[name$="-id"]');
            if (idInput && idInput.value) {
                row.style.display = 'none';
                row.querySelector('input[name$="-DELETE"]').checked = true;
            } else {
                row.remove();
                reindexNestedItems(card, '.attribute-list', 'attributes');
            }
        }

        // REMOVER IMAGEM DA VARIANTE
        // Supondo que o botão de remover imagem tenha a classe 'remove-image-btn'
        if (target.classList.contains('remove-image-btn') || target.closest('.remove-image-btn')) {
            const box = target.closest('.upload-box');
            const idInput = box.querySelector('input[name$="-id"]');
            if (idInput && idInput.value) {
                box.style.display = 'none';
                box.querySelector('input[name$="-DELETE"]').checked = true;
            } else {
                box.remove();
                reindexNestedItems(card, '.image-list', 'images');
            }
        }

        // REMOVER VARIANTE
        if (target.classList.contains('remove-variant')) {
            const idInput = card.querySelector('input[name$="-id"]');
            if (idInput && idInput.value) {
                if (confirm("Deseja marcar esta variante para exclusão?")) {
                    card.style.display = 'none';
                    card.querySelector('input[name$="-DELETE"]').checked = true;
                }
            } else {
                card.remove();
                reindexVariants();
            }
        }
    });

    /* --- 5. EVENTOS DE MUDANÇA --- */
    variantsContainer.addEventListener('change', (e) => {
        if (e.target.type === 'file') handleImagePreview(e.target);
        if (e.target.name.endsWith('-type')) updateVisibility(e.target.closest('.variant-card'));
    });

    // Inicializa campos existentes no carregamento
    document.querySelectorAll('.variant-card').forEach(updateVisibility);
});

/* --- PREVIEW DA IMAGEM PRINCIPAL DO PRODUTO --- */
function handleMainProductImagePreview(input) {
    if (!input.files || !input.files[0]) return;
    const uploadBox = document.getElementById('imageUploadBox');
    const uploadContent = document.getElementById('imageUploadContent');
    if (!uploadBox) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        let img = uploadBox.querySelector('.main-img-preview');
        if (!img) {
            img = document.createElement('img');
            img.className = 'main-img-preview';
            img.style.cssText = "width:135px; height:135px; object-fit:cover; border-radius:8px; display:block;";
            uploadBox.appendChild(img);
        }
        img.src = e.target.result;
        if (uploadContent) uploadContent.style.display = 'none';
    };
    reader.readAsDataURL(input.files[0]);
}