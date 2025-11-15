document.addEventListener('DOMContentLoaded', () => 
{
  const imageInput = document.getElementById("id_image");
  if (imageInput) {
    imageInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
          document.querySelector('.upload-content').innerHTML =
            `<img src="${event.target.result}" alt="Prévia" style="max-height:150px; border-radius:8px;">`;
        };
        reader.readAsDataURL(file);
      }
    });
  }
});

  // --- ⚙️ Controle de visibilidade de campos (days / stock / customizable) ---
  const days = document.querySelector('#div_id_production_days');
  const stock = document.querySelector('#div_id_stock');
  const customizable = document.querySelector('#div_id_is_customizable');
  const radios = document.querySelectorAll('input[name="type"]');

  [days, stock, customizable].forEach(el => el?.classList.add('transition-box'));

  function toggleBox(el, show) {
  if (!el) return;

  if (show) {
    el.classList.add("open");
    el.style.height = "auto";
    const height = el.scrollHeight + "px";
    el.style.height = "0px";

    requestAnimationFrame(() => {
      el.style.height = height;
    });

    el.addEventListener("transitionend", function handler() {
      el.style.height = "auto"; // libera o conteúdo
      el.removeEventListener("transitionend", handler);
    });

  } else {
    const height = el.scrollHeight + "px";
    el.style.height = height;

    requestAnimationFrame(() => {
      el.style.height = "0px";
      el.classList.remove("open");
    });
  }
}


  function updateVisibility() {
    const checked = document.querySelector('input[name="type"]:checked');
    if (checked && checked.value === 'DEMAND') {
      toggleBox(days, true);
      toggleBox(stock, false);
      toggleBox(customizable, true);
    } else {
      toggleBox(days, false);
      toggleBox(stock, true);
      toggleBox(customizable, false);
    }
  }

  radios.forEach(radio => radio.addEventListener('change', updateVisibility));
  updateVisibility();

  // --- 🧩 Atributos dinâmicos ---
  const attributeInput = document.querySelector('#id_attribute');
  const valueInput = document.querySelector('#id_value');
  const addButton = document.querySelector('#addButton');
  const attributeList = document.querySelector('#attributeList');
  const attributesData = document.querySelector('#attributesData');
  const formAttribute = document.querySelector('.attribute-form');

  let attributes = [];

  if (addButton) {
    addButton.addEventListener('click', (e) => {
      e.preventDefault();

      const attribute_id = attributeInput?.value.trim();
      const attribute_name = attributeInput?.options[attributeInput.selectedIndex]?.text;
      const value = valueInput?.value.trim();
      let errorMsg = formAttribute.querySelector('.text-danger');

if (!attribute_id || !attribute_name || !value) {

  if (!errorMsg) {
    errorMsg = document.createElement('span');
    errorMsg.classList.add('text-danger');
    formAttribute.insertBefore(errorMsg, addButton);
  }

  errorMsg.textContent = 'Por favor, selecione um atributo e/ou seu valor válidos.';
  return;
}

// Se chegou aqui, remover erro se existir
if (errorMsg) errorMsg.remove();

      // Cria o objeto e salva no array
      const newItem = { id: attribute_id, name: attribute_name, value };
      attributes.push(newItem);

      // Atualiza o campo hidden com o JSON
      attributesData.value = JSON.stringify(attributes);

      // Cria o bloco visual
      const newDiv = document.createElement('div');
      newDiv.classList.add('attribute-item');
      newDiv.innerHTML = `
      <div class="attribute-info">
        <p><strong>${attribute_name}</strong>: ${value}</p>
        <button type="button" class="btn btn-danger btn-sm remove-btn">Remover</button>
      </div>
      `;

      // Função de remover
      newDiv.querySelector('.remove-btn').addEventListener('click', () => {
        attributes = attributes.filter(item => !(item.attribute_id === attribute_id && item.value === value));
        attributesData.value = JSON.stringify(attributes);
        newDiv.remove();
      });

      // Adiciona visualmente
      attributeList.appendChild(newDiv);

      // Limpa os inputs
      attributeInput.value = '';
      valueInput.value = '';
    });
  }