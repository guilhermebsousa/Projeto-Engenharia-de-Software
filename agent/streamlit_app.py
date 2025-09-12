import streamlit as st
import os
from ai_stock_agent import AIStockAgent
from database.session import SessionLocal
from database.models.products import Product
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="🏪 Controle de Estoque IA",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.8rem;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-left: 4px solid #4f46e5;
    margin-left: 2rem;
}
.agent-message {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    border-left: 4px solid #ec4899;
    margin-right: 2rem;
}
.metric-card {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    border: 1px solid #dee2e6;
}

/* Estilização da barra de input do chat */
.stChatInput {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 999 !important;
    background: white !important;
    padding: 1rem 2rem !important;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1) !important;
    border-top: 2px solid #f0f2f6 !important;
}

.stChatInput > div {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

.stChatInput input {
    height: 60px !important;
    font-size: 16px !important;
    padding: 15px 20px !important;
    border-radius: 30px !important;
    border: 2px solid #e1e5e9 !important;
    background: #f8f9fa !important;
    transition: all 0.3s ease !important;
}

.stChatInput input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    background: white !important;
}

.stChatInput button {
    height: 50px !important;
    width: 50px !important;
    border-radius: 25px !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    margin-left: 10px !important;
    transition: all 0.3s ease !important;
}

.stChatInput button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
}

/* Adicionar espaço no final da página para a barra fixa */
body {
    padding-bottom: 120px !important;
}

.main .block-container {
    padding-bottom: 120px !important;
}
</style>
""", unsafe_allow_html=True)

# Função para inicializar o agente
@st.cache_resource
def init_agent():
    try:
        return AIStockAgent()
    except Exception as e:
        st.error(f"Erro ao inicializar o agente: {str(e)}")
        return None

# Função para buscar estatísticas do estoque
@st.cache_data
def get_stock_stats():
    db = SessionLocal()
    try:
        total_products = db.query(Product).count()
        low_stock = db.query(Product).filter(Product.current_quantity < Product.minimum_stock).count()
        out_of_stock = db.query(Product).filter(Product.current_quantity <= 0).count()
        
        return {
            "total_products": total_products,
            "low_stock": low_stock,
            "out_of_stock": out_of_stock
        }
    except Exception as e:
        st.error(f"Erro ao buscar estatísticas: {str(e)}")
        return {"total_products": 0, "low_stock": 0, "out_of_stock": 0}
    finally:
        db.close()

# Função para buscar produtos
@st.cache_data
def get_products_data():
    db = SessionLocal()
    try:
        products = db.query(Product).all()
        data = []
        for product in products:
            data.append({
                "Nome": product.name,
                "Marca": product.brand or "N/A",
                "Quantidade Atual": product.current_quantity,
                "Estoque Mínimo": product.minimum_stock,
                "Unidade": product.unit,
                "Preço Sugerido": f"R$ {product.suggested_price:.2f}" if product.suggested_price else "N/A",
                "Status": "🔴 Sem estoque" if product.current_quantity <= 0 
                         else "🟡 Estoque baixo" if product.current_quantity < product.minimum_stock 
                         else "🟢 OK"
            })
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Erro ao buscar produtos: {str(e)}")
        return pd.DataFrame()
    finally:
        db.close()

# Título principal
st.markdown('<h1 class="main-header">🏪 Sistema de Controle de Estoque com IA</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Menu")
page = st.sidebar.selectbox(
    "Escolha uma página:",
    ["🤖 Chat com IA", "📦 Visualizar Estoque", "📈 Dashboard"]
)

# Verificar configuração
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OPENAI_API_KEY não configurada! Verifique o arquivo .env")
    st.stop()

# Inicializar agente
agent = init_agent()
if not agent:
    st.error("❌ Não foi possível inicializar o agente de IA")
    st.stop()

# Página: Chat com IA
if page == "🤖 Chat com IA":
    st.header("💬 Converse com o Agente de IA")
    
    # Inicializar histórico de chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Olá! Sou seu assistente de estoque. Pergunte-me sobre produtos, quantidades, ou qualquer coisa relacionada ao seu estoque! 📦"
        })
    
    # Exibir histórico de chat
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>Você:</strong> {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message agent-message"><strong>🤖 Agente:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    
    # Input do usuário
    user_input = st.chat_input("Digite sua pergunta sobre o estoque...")
    
    if user_input:
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Processar pergunta
        with st.spinner("🤔 Processando sua pergunta..."):
            try:
                response = agent.process_question(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_msg = f"Desculpe, ocorreu um erro: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
        
        st.rerun()
    
    # Botão para limpar chat
    if st.button("🗑️ Limpar Chat"):
        st.session_state.messages = []
        st.rerun()

# Página: Visualizar Estoque
elif page == "📦 Visualizar Estoque":
    st.header("📦 Produtos em Estoque")
    
    # Buscar dados dos produtos
    df = get_products_data()
    
    if not df.empty:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("🔍 Buscar produto:", placeholder="Digite o nome do produto...")
        with col2:
            status_filter = st.selectbox("📊 Filtrar por status:", ["Todos", "🟢 OK", "🟡 Estoque baixo", "🔴 Sem estoque"])
        
        # Aplicar filtros
        filtered_df = df.copy()
        if search_term:
            filtered_df = filtered_df[filtered_df["Nome"].str.contains(search_term, case=False, na=False)]
        if status_filter != "Todos":
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        
        # Exibir tabela
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Botão para atualizar dados
        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear()
            st.rerun()
    else:
        st.info("📭 Nenhum produto encontrado no estoque.")

# Página: Dashboard
elif page == "📈 Dashboard":
    st.header("📈 Dashboard do Estoque")
    
    # Buscar estatísticas
    stats = get_stock_stats()
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📦 Total de Produtos",
            value=stats["total_products"]
        )
    
    with col2:
        st.metric(
            label="🟡 Estoque Baixo",
            value=stats["low_stock"],
            delta=f"-{stats['low_stock']}" if stats["low_stock"] > 0 else None
        )
    
    with col3:
        st.metric(
            label="🔴 Sem Estoque",
            value=stats["out_of_stock"],
            delta=f"-{stats['out_of_stock']}" if stats["out_of_stock"] > 0 else None
        )
    
    # Gráficos
    if stats["total_products"] > 0:
        st.subheader("📊 Distribuição do Status do Estoque")
        
        # Dados para o gráfico
        ok_products = stats["total_products"] - stats["low_stock"] - stats["out_of_stock"]
        chart_data = pd.DataFrame({
            "Status": ["🟢 OK", "🟡 Estoque Baixo", "🔴 Sem Estoque"],
            "Quantidade": [ok_products, stats["low_stock"], stats["out_of_stock"]]
        })
        
        st.bar_chart(chart_data.set_index("Status"))
    
    # Alertas
    if stats["out_of_stock"] > 0:
        st.error(f"⚠️ ATENÇÃO: {stats['out_of_stock']} produto(s) sem estoque!")
    
    if stats["low_stock"] > 0:
        st.warning(f"⚠️ AVISO: {stats['low_stock']} produto(s) com estoque baixo!")
    
    if stats["out_of_stock"] == 0 and stats["low_stock"] == 0:
        st.success("✅ Todos os produtos estão com estoque adequado!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>""🤖 Sistema de Controle de Estoque com IA | Desenvolvido com Streamlit""</div>",
    unsafe_allow_html=True
)