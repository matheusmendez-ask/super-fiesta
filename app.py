import urllib.parse
import os
# os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

import secrets
import streamlit as st
from decimal import Decimal
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import requests
import json

# Configuração da Página
st.set_page_config(
    page_title="Simulador Financeiro",
    page_icon="💼",
    layout="wide"
)

# CONFIGURAÇÃO DE ESTILO
st.markdown("""
<style>
    :root {
        --primary-color: #1f77b4;
        --background-color: #FFFFFF;
        --border-color: #e0e0e0;
        --shadow-color: rgba(0,0,0,0.1);
        --primary-text-color: #2c3e50;
        --secondary-text-color: #666;
    }

    @media (prefers-color-scheme: dark) {
        :root {
            --primary-color: #29b6f6;
            --background-color: #1e1e1e;
            --border-color: #424242;
            --shadow-color: rgba(255,255,255,0.1);
            --primary-text-color: #ffffff;
            --secondary-text-color: #b0b0b0;
        }
    }

    .custom-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: var(--background-color);
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px var(--shadow-color);
    }

    .custom-card h3 {
        color: var(--primary-text-color) !important;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 0.5rem;
    }

    .custom-card div {
        color: var(--secondary-text-color);
        font-size: 14px;
    }

    .custom-card strong {
        color: var(--primary-text-color);
    }

    .custom-card hr {
        border-color: var(--border-color);
        margin: 1rem 0;
    }

    .footer {
        text-align: center;
        padding: 1rem;
        color: var(--secondary-text-color);
        font-size: 0.9rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

FINANCEIRAS = [
    {
        "Nome": "Santander",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 1500.00,
        "RecebivelMax": 100000000.00,
        "Parcelas": (3, 60),
        "Taxa": 0.0224,
        "Parentesco": "Parentes de primeiro grau",
        "TAC": {"PF": 930.00, "PJ": 1200.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Santander",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 1500.00,
        "RecebivelMax": 100000000.00,
        "Parcelas": (3, 60),
        "Taxa": 0.0224,
        "Parentesco": "Profissional",
        "TAC": {"PF": 930.00, "PJ": 1200.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Medical San",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 1000.00,
        "RecebivelMax": 100000000.00,
        "Parcelas": (1, 36),
        "Taxa": 0.0209,
        "Parentesco": "Parentes de primeiro grau",
        "TAC": {"PF": 1000.00, "PJ": 1000.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Medical San",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 1000.00,
        "RecebivelMax": 100000000.00,
        "Parcelas": (1, 36),
        "Taxa": 0.0209,
        "Parentesco": "Profissional",
        "TAC": {"PF": 1000.00, "PJ": 1000.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "BMP",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 1500.00,
        "RecebivelMax": 100000000.00,
        "Parcelas": (1, 36),
        "Taxa": {12: 0.0399, 18: 0.0349, 24: 0.0319, 36: 0.0279},
        "Parentesco": "Profissional",
        "TAC": {"PF": 830.00, "PJ": 830.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Hubcred",
        "Tipos": ["PF"],
        "RecebivelMin": 500.00,
        "RecebivelMax": 30000.00,
        "Parcelas": (12, 18),
        "Taxa": 0.03,
        "Parentesco": "Flexivel",
        "TAC": {"PF": 299.00, "PJ": 299.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "ATF",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 4000.00,
        "RecebivelMax": 30000.00,
        "Parcelas": (1, 36),
        "Taxa": {24: 0.0259, 36: 0.0249},
        "Parentesco": "Profissional",
        "TAC": {"PF": 375.00, "PJ": 375.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Baru",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 30000.00,
        "RecebivelMax": 500000.00,
        "Parcelas": (24, 48),
        "Taxa": 0.0259,
        "Parentesco": "Parentes de primeiro grau",
        "TAC": {"PF": 1500.00, "PJ": 1500.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Baru",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 30000.00,
        "RecebivelMax": 500000.00,
        "Parcelas": (24, 48),
        "Taxa": 0.0259,
        "Parentesco": "Profissional",
        "TAC": {"PF": 1500.00, "PJ": 1500.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Gloria",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 1500.00,
        "RecebivelMax": 100000000.00,
        "Parcelas": (1, 36),
        "Taxa": {12: 0.0399, 18: 0.0349, 24: 0.0299, 36: 0.0279},
        "Parentesco": "Profissional",
        "TAC": {"PF": 830.00, "PJ": 830.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Sicoob PF",
        "Tipos": ["PF"],
        "RecebivelMin": 1500.00,
        "RecebivelMax": 100000000.00,
        "Parcelas": (1, 48),
        "Taxa": {12: 0.0162, 18: 0.0166, 24: 0.0166, 36: 0.0180, 48: 0.0175},
        "Parentesco": "Profissional",
        "TAC": {"PF": 0.00, "PJ": 0.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Sicoob PJ",
        "Tipos": ["PJ"],
        "RecebivelMin": 1500.00,
        "RecebivelMax": 100000000.00,
        "Parcelas": (1, 48),
        "Taxa": {12: 0.0160, 18: 0.0164, 24: 0.0164, 36: 0.0168, 48: 0.0172},
        "Parentesco": "Profissional",
        "TAC": {"PF": 0.00, "PJ": 0.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    }
]

# Substitua estas configurações
CLIENT_ID = st.secrets.google_auth.client_id
CLIENT_SECRET = st.secrets.google_auth.client_secret
REDIRECT_URI = st.secrets.google_auth.redirect_uri  # Ou http://localhost:8501 para local
SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.email"]

def get_flow():
    return Flow.from_client_config(
        client_config={
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def login_button():
    flow = get_flow()
    authorization_url, state = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        state=secrets.token_urlsafe(16)  # Corrigido
    )
    st.session_state.oauth_state = state
    st.markdown(f"""
    <a href="{authorization_url}" target="_self">
        <button style="
            background: #4285F4;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;">
            🔑 Login com Google
        </button>
    </a>
    """, unsafe_allow_html=True)

def handle_callback():
    try:
        # Verifique se 'code' e 'state' estão presentes
        if 'code' not in st.query_params or 'state' not in st.query_params:
            st.error("Parâmetros de autenticação ausentes")
            return

        # Construa a URL de callback dinamicamente
        protocol = "https"
        host = st.secrets.google_auth.redirect_uri.split("//")[-1].split("/")[0]
        full_url = f"{protocol}://{host}/?{urllib.parse.urlencode(st.query_params, doseq=True)}"

        # Autenticação
        flow = get_flow()
        flow.fetch_token(authorization_response=full_url)
        
        # Obtenha dados do usuário
        credentials = flow.credentials
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {credentials.token}"}
        ).json()
        
        # Atualize a sessão
        st.session_state.update({
            'logged_in': True,
            'user_email': user_info["email"],
            'user_name': user_info.get("name", "Usuário")
        })
        
        st.query_params.clear()  # Limpe a URL
        
    except Exception as e:
        st.error(f"Erro de autenticação: {str(e)}")
        st.stop()

# Verificação de Login
if not st.session_state.get('logged_in'):
    if 'code' in st.query_params:
        handle_callback()
    else:
        st.title("🔒 Login Necessário")
        login_button()
        st.stop()

# Se logado, mostrar o conteúdo principal
st.title("💰 Simulador Financeiro")
st.write(f"Bem-vindo, {st.session_state.user_name}!")
logout = st.button("Sair")
if logout:
    st.session_state.clear()
    st.experimental_rerun()

st.markdown(f"**Usuário:** {st.session_state.user_name} | {st.session_state.user_email}")

if logout:
    st.session_state.clear()
    st.experimental_rerun()

st.title("💰 Simulador de Financiamento Inteligente")
st.markdown("---")

with st.container():
    st.header("📋 Preencha os Dados da Operação")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        valor = st.number_input("Recebível (R$)", 
                              min_value=500.0,
                              max_value=100000000.0,
                              step=1000.0,
                              format="%.2f")
        
    with col2:
        tipo_cliente = st.selectbox("Tipo do Cliente", ["PF", "PJ"])
        
    with col3:
        parentesco = st.selectbox("Destinação do Crédito", 
                                ["Profissional", "Parentes de 1º Grau", "Flexivel"])

st.markdown("---")
with st.container():
    st.header("📅 Condições de Pagamento")
    # Ajuste do slider para incluir 24 até 48
    parcelas = st.slider("Número de Parcelas", 
                       min_value=1,
                       max_value=60,
                       value=24,  # Valor padrão alterado para 24
                       help="Selecione o prazo desejado para pagamento")

resultados = []

for financeira in FINANCEIRAS:
    try:
        if tipo_cliente not in financeira["Tipos"]:
            continue
            
        if not (financeira["RecebivelMin"] <= valor <= financeira["RecebivelMax"]):
            continue
            
        min_p, max_p = financeira["Parcelas"]
        if not (min_p <= parcelas <= max_p):
            continue
            
        # Correção na comparação de Parentesco
        if parentesco == "Parentes de 1º Grau":
            if financeira["Parentesco"] != "Parentes de primeiro grau":
                continue
        elif parentesco == "Flexivel":
            if financeira["Parentesco"] != "Flexivel":
                continue
        else:  # Profissional
            if financeira["Parentesco"] != "Profissional":
                continue
                
        if isinstance(financeira["Taxa"], dict):
            taxa = next((v for k, v in sorted(financeira["Taxa"].items()) if parcelas <= k), 0.0)
        else:
            taxa = financeira["Taxa"]
            
        tac = financeira["TAC"][tipo_cliente]
        iof = financeira["IOF"][tipo_cliente]
        
        def calcular_parcela(valor_principal, taxa_mensal, tac, iof, parcelas):
            """
            Calcula o valor da parcela usando a fórmula Price correta
            """
            valor_principal = Decimal(str(valor_principal))
            taxa_mensal = Decimal(str(taxa_mensal))
            tac = Decimal(str(tac))
            iof = Decimal(str(iof))
            parcelas = Decimal(str(parcelas))

            # Adiciona TAC ao valor financiado (correção importante!)
            valor_financiado = valor_principal + tac  # Alteração aqui

            # Calcula IOF sobre o valor financiado
            valor_com_iof = valor_financiado * (1 + iof)

            # Fator Price
            fator = (taxa_mensal * (1 + taxa_mensal)**parcelas) / ((1 + taxa_mensal)**parcelas - 1)

            # Parcela
            parcela = valor_com_iof * fator
            return parcela.quantize(Decimal('0.01'))
                
        # Na seção de cálculos, substitua por:
        valor_parcela = calcular_parcela(
            valor_principal=Decimal(valor),
            taxa_mensal=Decimal(taxa),
            tac=Decimal(tac),
            iof=Decimal(iof),
            parcelas=Decimal(parcelas)
        )
        valor_total = valor_parcela * parcelas
        
        resultados.append({
            "Nome": financeira["Nome"],
            "Taxa": taxa * 100,
            "Parcela": formatar_moeda(valor_parcela),
            "Total": formatar_moeda(valor_total),
            "TAC": formatar_moeda(tac),
            "IOF": f"{iof * 100:.1f}%"
        })
    except Exception as e:
        continue

st.markdown("---")
st.header("📊 Resultados das Simulações")

if resultados:
    # Encontrar melhor e pior parcela
    def parse_valor_parcela(valor_formatado):
        return float(valor_formatado.replace("R$ ", "").replace(".", "").replace(",", "."))
    
    # Extrair valores numéricos das parcelas
    parcelas_numericas = [parse_valor_parcela(r['Parcela']) for r in resultados]
    
    melhor_idx = parcelas_numericas.index(min(parcelas_numericas))
    pior_idx = parcelas_numericas.index(max(parcelas_numericas))

    # Seção de Melhor/Pior
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Melhor Oferta")
        melhor = resultados[melhor_idx]
        st.markdown(f"""
        <div class='custom-card' style='border: 2px solid #4CAF50;'>
            <h3 style='color: #4CAF50 !important;'>{melhor['Nome']}</h3>
            <div>📆 Parcelas: <strong>{parcelas}x</strong></div>
            <div>💵 Taxa: <strong>{melhor['Taxa']:.2f}%</strong></div>
            <div>💸 Parcela: <strong style='font-size: 1.2em;'>{melhor['Parcela']}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("⚠️ Maior Parcela")
        pior = resultados[pior_idx]
        st.markdown(f"""
        <div class='custom-card' style='border: 2px solid #F44336;'>
            <h3 style='color: #F44336 !important;'>{pior['Nome']}</h3>
            <div>📆 Parcelas: <strong>{parcelas}x</strong></div>
            <div>💵 Taxa: <strong>{pior['Taxa']:.2f}%</strong></div>
            <div>💸 Parcela: <strong style='font-size: 1.2em;'>{pior['Parcela']}</strong></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Todas as Opções Disponíveis")

    # Lista completa de resultados
    cols = st.columns(len(resultados))
    for idx, resultado in enumerate(resultados):
        with cols[idx]:
            badge = ""
            if idx == melhor_idx:
                badge = "<span style='background: #4CAF50; color: white; padding: 0.2rem 0.5rem; border-radius: 5px; font-size: 0.8em; margin-left: 0.5rem;'>MELHOR</span>"
            elif idx == pior_idx:
                badge = "<span style='background: #F44336; color: white; padding: 0.2rem 0.5rem; border-radius: 5px; font-size: 0.8em; margin-left: 0.5rem;'>MAIOR</span>"
            
            st.markdown(f"""
            <div class='custom-card'>
                <h3>{resultado['Nome']}{badge}</h3>
                <div>
                    <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                        <span>📆 Parcelas:</span>
                        <strong>{parcelas}x</strong>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                        <span>💵 Taxa Mensal:</span>
                        <strong>{resultado['Taxa']:.2f}%</strong>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                        <span>💸 Valor Parcela:</span>
                        <strong>{resultado['Parcela']}</strong>
                    </div>
                    <hr>
                    <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                        <span>📝 TAC:</span>
                        <strong>{resultado['TAC']}</strong>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                        <span>📈 IOF:</span>
                        <strong>{resultado['IOF']}</strong>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                        <span>💰 Total:</span>
                        <strong style='color: var(--primary-color);'>{resultado['Total']}</strong>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Nenhuma opção disponível para os critérios selecionados")

st.markdown("---")
st.markdown("""
<div class="footer">
    © 2024 Simulador Financeiro | Todos os valores são ilustrativos e sujeitos à confirmação
</div>
""", unsafe_allow_html=True)
