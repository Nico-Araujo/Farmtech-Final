import streamlit as st
import pandas as pd
from PIL import Image
import os

# Importando os módulos das fases
from fases import fase1_calc, fase2_db, fase3_iot, fase6_vision, fase5_cloud

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="FarmTech Solutions",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS ---
st.markdown("""
<style>
    /* 1. Cor de Fundo Geral (#00643e) */
    .stApp {
        background-color: #00643e;
        color: white; /* Texto branco para contraste */
    }
    
    /* 2. Cor do Menu Lateral (#007d4d) */
    [data-testid="stSidebar"] {
        background-color: #007d4d;
        border-right: 1px solid #004d2f;
    }
    
    /* Força texto branco no Sidebar */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Estilo dos Títulos (Agora Brancos) */
    .main-header {
        font-size: 2.5rem; 
        color: #FFFFFF;
        text-align: center;
        font-weight: bold;
    }
    
    h1, h2, h3 {
        color: #FFFFFF !important;
    }
    
    /* Cartões de Métricas (Números em Amarelo Ouro) */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #FBC02D !important; /* Amarelo destaca muito bem no verde */
        font-weight: bold;
    }
    
    /* Label da métrica (Ex: "Temp. Motor") em cinza claro */
    [data-testid="stMetricLabel"] {
        color: #E0E0E0 !important;
        font-weight: 500;
    }
    
    /* Ajuste para inputs ficarem legíveis */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    try:
        # LOGO: Ícone de folha/natureza
        st.image("https://cdn-icons-png.flaticon.com/512/2913/2913520.png", width=100)
    except:
        st.write("🌱")
        
    st.title("FarmTech 🚜")
    st.markdown("**Sistema Integrado de Gestão**")
    st.divider()
    
    menu = st.radio(
        "Navegação:",
        ["🏠 Home", "🌱 Fase 1: Plantio", "🗄️ Fase 2: Banco de Dados", 
         "📡 Fase 3: IoT & Monitoramento", "👁️ Fase 6: Visão Computacional"]
    )
    
    st.divider()
    st.info("👨‍💻 Projeto Fase 7 - Consolidação")

# --- HOME ---
if menu == "🏠 Home":
    st.markdown("<h1 class='main-header'>Bem-vindo à FarmTech Solutions</h1>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Sistema Integrado de Gestão Agrícola e Monitoramento IoT.**")
        st.markdown("""
        * **Fase 1:** Planejamento de Plantio (Cálculo Automático)
        * **Fase 2:** Banco de Dados (Gestão de Estoque)
        * **Fase 3:** Sensores IoT (Simulação em Tempo Real)
        * **Fase 6:** I.A. Visão Computacional (Segurança)
        """)
    with col2:
        st.success("✅ Sistema Operacional. Selecione um módulo no menu lateral.")

# --- FASE 1 (COM LÓGICA DE PRESETS) ---
elif menu == "🌱 Fase 1: Plantio":
    st.header("🌱 Planejamento de Plantio")
    st.markdown("---")
    
    presets = {
        "Soja": {"qtd": 0.50, "insumo": "Fertilizante NPK"},
        "Milho": {"qtd": 0.80, "insumo": "Ureia"},
        "Feijão": {"qtd": 0.40, "insumo": "Adubo Orgânico"},
        "Cana-de-Açúcar": {"qtd": 1.20, "insumo": "Calcário"},
        "Algodão": {"qtd": 0.65, "insumo": "Defensivo X"}
    }
    
    col1, col2 = st.columns(2)
    with col1:
        cultura_selecionada = st.selectbox("Selecione a Cultura", list(presets.keys()))
        dados_cultura = presets[cultura_selecionada]
        
        forma = st.selectbox("Formato do Terreno", ["Retângulo", "Quadrado", "Círculo"])
        dim1 = st.number_input("Dimensão 1 (m)", value=100.0)
        dim2 = st.number_input("Dimensão 2 (m)", value=50.0) if forma == "Retângulo" else 0.0
        
    with col2:
        st.subheader("Configuração de Insumos")
        insumo = st.text_input("Insumo Principal", value=dados_cultura["insumo"])
        qtd = st.number_input(f"Qtd recomendada por m² (kg/L)", value=dados_cultura["qtd"], format="%.2f")
        st.caption(f"💡 Dica: {cultura_selecionada} geralmente requer {dados_cultura['qtd']} kg/m².")
        
    if st.button("Calcular Planejamento"):
        area = fase1_calc.calcular_area_plantio(forma, dim1, dim2)
        total = fase1_calc.calcular_qtd_insumos(area, qtd, 1)
        
        st.markdown("### 📊 Resultados Estimados")
        c1, c2 = st.columns(2)
        c1.metric("Área Total", f"{area:,.2f} m²")
        c2.metric(f"Total de {insumo}", f"{total:,.2f} kg/L")

# --- FASE 2 ---
elif menu == "🗄️ Fase 2: Banco de Dados":
    st.header("🗄️ Gestão de Insumos")
    st.markdown("---")
    
    df, msg = fase2_db.obter_dados_insumos()
    
    if "Offline" in msg:
        st.warning(f"⚠️ Status: {msg}")
    else:
        st.success(f"✅ Status: {msg}")
        
    st.dataframe(df, use_container_width=True)
    
    st.markdown("### ➕ Cadastrar Novo Item")
    with st.form("db_form"):
        c1, c2 = st.columns(2)
        with c1:
            nome = st.text_input("Nome do Produto")
            tipo = st.selectbox("Categoria", ["Grão", "Fertilizante", "Defensivo", "Maquinário"])
        with c2:
            qtd = st.number_input("Quantidade em Estoque", min_value=1, step=1)
            val = st.date_input("Data de Validade")
            
        submitted = st.form_submit_button("Salvar no Banco de Dados")
        
        if submitted:
            if nome:
                resp = fase2_db.inserir_insumo(nome, tipo, qtd, str(val))
                if "Sucesso" in resp:
                    st.success(f"✅ {resp}")
                    st.rerun() 
                else:
                    st.error(f"❌ {resp}")
            else:
                st.warning("⚠️ Por favor, digite o nome do produto.")

# --- FASE 3 ---
elif menu == "📡 Fase 3: IoT & Monitoramento":
    st.header("📡 Monitoramento em Tempo Real")
    st.markdown("---")
    
    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("🔄 Atualizar Leitura"):
            st.rerun()
            
    # 1. Obter Dados
    dados = fase3_iot.get_dados_sensores()
    
    # 2. Exibir Métricas Formatadas
    temp = float(dados.get('maquina_temp', 0))
    vibra = float(dados.get('maquina_vibracao', 0))
    umid = float(dados.get('solo_umidade', 0))
    ph = float(dados.get('solo_ph', 0))

    col1, col2, col3, col4 = st.columns(4)
    # Cores
    col1.metric("🌡️ Temp. Motor", f"{temp:.1f} °C")      
    col2.metric("〰️ Vibração", f"{vibra:.3f} mm/s")    
    col3.metric("💧 Umidade Solo", f"{umid:.1f} %")       
    col4.metric("🧪 pH Solo", f"{ph:.1f}")               
    
    st.caption(f"Fonte dos dados: {dados.get('fonte_maquina', 'Simulado')}")
    
    # 3. Análise
    analise = fase3_iot.avaliar_irrigacao(dados)
    
    st.divider()
    if analise['alerta_critico']:
        st.error(f"### {analise['acao']}")
        st.markdown(f"**Motivo:** {analise['mensagem']}")
        with st.expander("☁️ Ver Log AWS (Fase 5)"):
            st.write(fase5_cloud.enviar_alerta_aws("Alerta Crítico", analise['mensagem']))
    else:
        st.success(f"### {analise['acao']}")
        st.write(f"**Status:** {analise['mensagem']}")

# --- FASE 6 ---
elif menu == "👁️ Fase 6: Visão Computacional":
    st.header("👁️ Monitoramento de Campo (Segurança)")
    st.markdown("---")
    st.info("Detecção automática de agricultores e maquinário para segurança do trabalho.")
    
    arquivo = st.file_uploader("Envie uma imagem da plantação", type=["jpg", "png", "jpeg"])
    
    if arquivo:
        img = Image.open(arquivo)
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(img, caption="Imagem Original", use_column_width=True)
            
        if st.button("🔍 Iniciar Varredura"):
            with st.spinner("Analisando perímetro com I.A..."):
                res_img, txt = fase6_vision.processar_imagem(img)
                
                with col2:
                    st.image(res_img, caption="Resultado da Análise", use_column_width=True)
                    if "✅" in txt:
                        st.success(txt)
                    else:

                        st.warning(txt)
