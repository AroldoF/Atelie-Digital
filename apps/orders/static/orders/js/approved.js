// Dados do pedido (podem vir de uma API ou backend)
const orderData = {
    orderId: "AT001235",
    storeName: "Ateliê da Maria",
    products: [
        { id: "1", name: "Vaso de Cerâmica Artesanal", quantity: 2, price: 89.90 },
        { id: "2", name: "Prato Decorativo Pintado à Mão", quantity: 1, price: 145.00 },
        { id: "3", name: "Jogo de Xícaras Rústicas", quantity: 1, price: 210.00 }
    ]
};

// Formatar valor em reais
function formatCurrency(value) {
    return "R$ " + value.toFixed(2).replace(".", ",");
}

// Renderizar lista de produtos
function renderProducts(products) {
    const productsList = document.getElementById("productsList");
    
    products.forEach(product => {
        const li = document.createElement("li");
        li.className = "product-item";
        
        const subtotal = product.price * product.quantity;
        
        li.innerHTML = `
            <div class="product-info">
                <span class="product-quantity">${product.quantity}x</span>
                <span class="product-name">${product.name}</span>
            </div>
            <span class="product-price">${formatCurrency(subtotal)}</span>
        `;
        
        productsList.appendChild(li);
    });
}

// Calcular e exibir total
function calculateTotal(products) {
    const total = products.reduce((acc, product) => {
        return acc + (product.price * product.quantity);
    }, 0);
    
    document.getElementById("totalValue").textContent = formatCurrency(total);
}

// Atualizar número do pedido
function updateOrderId(orderId) {
    const tagOrder = document.querySelector(".tag_order");
    if (tagOrder) {
        tagOrder.textContent = "#" + orderId;
    }
}

// Atualizar nome da loja
function updateStoreName(storeName) {
    const storeNameElement = document.querySelector(".store-name");
    if (storeNameElement) {
        storeNameElement.textContent = storeName;
    }
}

// Inicialização
document.addEventListener("DOMContentLoaded", function() {
    // Atualizar dados na página
    updateOrderId(orderData.orderId);
    updateStoreName(orderData.storeName);
    renderProducts(orderData.products);
    calculateTotal(orderData.products);
    
    // Event listeners para os botões
    const btnPrimary = document.querySelector(".btn-primary");
    const btnSecondary = document.querySelector(".btn-secondary");
    
    if (btnPrimary) {
        btnPrimary.addEventListener("click", function() {
            // Navegar para detalhes do pedido
            alert("Redirecionando para detalhes do pedido #" + orderData.orderId);
            // window.location.href = "/pedidos/" + orderData.orderId;
        });
    }
    
    if (btnSecondary) {
        btnSecondary.addEventListener("click", function() {
            // Voltar para a loja
            alert("Voltando para a loja");
            // window.location.href = "/";
        });
    }
});