import streamlit as st
import os
import sys
from datetime import datetime

# Adicionar o diretório pai ao path para permitir imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_stock_agent import AIStockAgent

# Configuração da página
st.set_page_config(
    page_title="🤖 Chatbot de Estoque IA",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para o chatbot
st.markdown("""
<style>
/* Fundo geral preto */
.stApp {
    background-color: #000000 !important;
}

.main .block-container {
    background-color: #000000 !important;
    padding-top: 1rem;
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Sidebar preta */
.css-1d391kg, .css-1lcbmhc {
    background-color: #000000 !important;
}

.main-header {
    font-size: 3rem;
    color: #ffffff;
    text-align: center;
    margin-bottom: 2rem;
    font-weight: bold;
}

.chat-container {
    max-height: 60vh;
    overflow-y: auto;
    padding: 1rem;
    background-color: #000000 !important;
    margin-bottom: 1rem;
    border: none;
}

.chat-message {
    padding: 1rem;
    border-radius: 15px;
    margin: 1rem 0;
    background-color: transparent !important;
    box-shadow: none;
    animation: fadeIn 0.5s ease-in;
    color: #ffffff !important;
    border: 2px solid #ffffff;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-message {
    background-color: transparent !important;
    color: #ffffff !important;
    margin-left: 20%;
    border: 2px solid #ffffff;
    text-align: right;
}

.bot-message {
    background-color: transparent !important;
    color: #ffffff !important;
    margin-right: 20%;
    border: 2px solid #ffffff;
    text-align: left;
}

.typing-indicator {
    background: #e9ecef;
    color: #6c757d;
    margin-right: 20%;
    border-bottom-left-radius: 5px;
    font-style: italic;
}

.chat-input-container {
    position: sticky;
    bottom: 0;
    background-color: #000000 !important;
    padding: 1rem 0;
    border-top: none !important;
    margin-top: 1rem;
}

/* Input field styling */
.stTextInput > div > div > input {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: 2px solid #ffffff !important;
    border-radius: 25px;
    padding: 12px 20px !important;
    font-size: 16px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ffffff !important;
    box-shadow: 0 0 0 2px #ffffff !important;
    background-color: #000000 !important;
}

/* Button styling */
.stButton > button {
    background-color: #000000 !important;
    color: #ffffff !important;
    border: 2px solid #ffffff !important;
    border-radius: 25px;
    padding: 12px 24px !important;
    font-weight: bold;
    font-size: 14px !important;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #333333 !important;
    border-color: #ffffff !important;
    color: #ffffff !important;
    transform: scale(1.05);
}

.stTextInput > div > div > input {
    border-radius: 25px;
    border: 2px solid #e1e5e9;
    padding: 12px 20px;
    font-size: 16px;
}

.stTextInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.send-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
}

.send-button:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.sidebar-info {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    border-left: 4px solid #2E86AB;
    margin: 1rem 0;
}

.status-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 8px;
}

.status-online {
    background-color: #28a745;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

.clear-chat-btn {
    background: #dc3545;
    color: white;
    border: none;
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.clear-chat-btn:hover {
    background: #c82333;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# Função para inicializar o agente
@st.cache_resource
def init_agent():
    try:
        return AIStockAgent()
    except Exception as e:
        st.error(f"❌ Erro ao inicializar o agente: {str(e)}")
        return None

# Função para exibir mensagens do chat
def display_chat_message(role, content, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    if role == "user":
        st.markdown(f'''
        <div class="chat-message user-message">
            <strong>👤 Você</strong> <small>({timestamp})</small><br>
            {content}
        </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
        <div class="chat-message bot-message">
            <strong>🤖 Assistente de Estoque</strong> <small>({timestamp})</small><br>
            {content}
        </div>
        ''', unsafe_allow_html=True)

# Função para exibir indicador de digitação
def show_typing_indicator():
    st.markdown('''
    <div class="chat-message typing-indicator">
        <strong>🤖 Assistente de Estoque</strong> está digitando...
        <span style="animation: blink 1.5s infinite;">●●●</span>
    </div>
    <style>
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    </style>
    ''', unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">🤖 Chatbot de Controle de Estoque</h1>', unsafe_allow_html=True)

# Sidebar com informações
with st.sidebar:
    st.title("ℹ️ Informações")
    
    # Status do sistema
    st.markdown('''
    <div class="sidebar-info">
        <h4>📊 Status do Sistema</h4>
        <p><span class="status-indicator status-online"></span>Chatbot Online</p>
        <p><span class="status-indicator status-online"></span>Banco de Dados Conectado</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Comandos disponíveis
    st.markdown('''
    <div class="sidebar-info">
        <h4>💡 Exemplos de Perguntas</h4>
        <ul>
            <li>"Quantos produtos temos em estoque?"</li>
            <li>"Quais produtos estão com estoque baixo?"</li>
            <li>"Mostre produtos da marca X"</li>
            <li>"Qual o estoque do produto Y?"</li>
            <li>"Produtos que vencem em breve"</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    
    # Informações técnicas
    st.markdown('''
    <div class="sidebar-info">
        <h4>🔧 Informações Técnicas</h4>
        <p><strong>Modelo:</strong> GPT-3.5-turbo</p>
        <p><strong>Banco:</strong> SQLite</p>
        <p><strong>Framework:</strong> Streamlit</p>
    </div>
    ''', unsafe_allow_html=True)

# Verificar configuração da API
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY não configurada! Verifique o arquivo .env")
    st.info("💡 Crie um arquivo .env na raiz do projeto com: OPENAI_API_KEY=sua_chave_aqui")
    st.stop()

# Inicializar agente
agent = init_agent()
if not agent:
    st.error("❌ Não foi possível inicializar o agente de IA")
    st.stop()

# Inicializar histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Olá! 👋 Sou seu assistente inteligente de controle de estoque. Posso ajudá-lo com informações sobre produtos, quantidades, marcas e muito mais! Como posso ajudá-lo hoje?",
        "timestamp": datetime.now().strftime("%H:%M")
    })

# Container principal do chat
chat_container = st.container()

with chat_container:
    # Área de mensagens
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Exibir histórico de mensagens
    for message in st.session_state.messages:
        display_chat_message(
            message["role"], 
            message["content"], 
            message.get("timestamp")
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Área de input (sempre visível na parte inferior)
st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns([6, 1, 1])

with col1:
    user_input = st.text_input(
        "Digite sua pergunta...",
        placeholder="Ex: Quantos produtos temos em estoque?",
        key="chat_input",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("📤 Enviar", key="send_btn", use_container_width=True)

with col3:
    clear_button = st.button("🗑️ Limpar", key="clear_btn", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Processar input do usuário
if (send_button and user_input) or (user_input and st.session_state.get("enter_pressed")):
    if user_input.strip():
        # Adicionar mensagem do usuário
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })
        
        # Mostrar indicador de digitação
        with st.spinner("🤔 Processando sua pergunta..."):
            try:
                # Processar pergunta com o agente
                response = agent.process_question(user_input)
                
                # Adicionar resposta do assistente
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
                
            except Exception as e:
                error_msg = f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%H:%M")
                })
        
        # Recarregar a página para limpar o input automaticamente
        st.rerun()

# Limpar chat
if clear_button:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "Chat limpo! 🧹 Como posso ajudá-lo agora?",
        "timestamp": datetime.now().strftime("%H:%M")
    }]
    st.rerun()

# Auto-scroll para a última mensagem
if st.session_state.messages:
    st.markdown("""
    <script>
    var chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    </script>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "🤖 Chatbot de Controle de Estoque | Desenvolvido com Streamlit e OpenAI"
    "</div>",
    unsafe_allow_html=True
)