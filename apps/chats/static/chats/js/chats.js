document.addEventListener('DOMContentLoaded', function() {
    const chatItems = document.querySelectorAll('.conversation-item');
    const chatArea = document.querySelector('.chat-area');
    const chatList = document.querySelector('.chat-list');
    const backBtn = document.querySelector('.back-button');
    const chatMessages = document.querySelector('.chat-messages');
    const messageInput = document.querySelector('.message-input');
    const sendButton = document.querySelector('.send-button');
    
    // Mostrar área de chat ao clicar em uma conversa
    chatItems.forEach(item => {
        item.addEventListener('click', function() {
            // Atualizar estado visual
            chatItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // Atualizar dados do cabeçalho
            const name = this.querySelector('.conversation-name').textContent;
            document.querySelector('.chat-header-title h6').textContent = name;
            
            // Remover placeholder e mostrar mensagens de exemplo
            chatMessages.innerHTML = `
                <div class="message message-received">
                    <div class="message-bubble">
                        Oi! Tudo bem?
                        <div class="message-time">10:15 AM</div>
                    </div>
                </div>
                <div class="message message-sent">
                    <div class="message-bubble">
                        Opa
                        <div class="message-time">10:15 AM</div>
                    </div>
                </div>
                <div class="message message-received">
                    <div class="message-bubble">
                        Fala patrão
                        <div class="message-time">10:17 AM</div>
                    </div>
                </div>
            `;
            
            // Lógica responsiva
            if (window.innerWidth < 768) {
                // Em mobile: ocultar lista e mostrar área de conversa
                chatList.classList.add('hidden');
                chatArea.classList.add('visible');
            } else {
                // Em desktop: garantir que ambos estejam visíveis
                chatList.classList.remove('hidden');
                chatArea.classList.remove('visible');
                chatArea.style.display = 'flex';
            }
        });
    });
    
    // Voltar para a lista em mobile
    backBtn?.addEventListener('click', function() {
        chatList.classList.remove('hidden');
        chatArea.classList.remove('visible');
    });
    
    // Enviar mensagem
    sendButton.addEventListener('click', function() {
        sendMessage();
    });
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            // Criar nova mensagem
            const messageElement = document.createElement('div');
            messageElement.className = 'message message-sent';
            messageElement.innerHTML = `
                <div class="message-bubble">
                    ${message}
                    <div class="message-time">Agora</div>
                </div>
            `;
            
            chatMessages.appendChild(messageElement);
            messageInput.value = '';
            
            // Scroll automático
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
});