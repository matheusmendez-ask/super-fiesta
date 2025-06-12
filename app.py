import streamlit as st
from decimal import Decimal

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
    
    .login-container {
        max-width: 450px;
        margin: 2rem auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px var(--shadow-color);
        background-color: var(--background-color);
    }
    
    .login-button {
        width: 100%;
        padding: 0.6rem;
        margin-top: 1rem;
        background-color: var(--primary-color);
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

FINANCEIRAS = [
    {
        "Nome": "Santander",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 30000.00,
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
        "RecebivelMin": 30000.00,
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
        "Nome": "Medical San",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 1000.00,
        "RecebivelMax": 100000000.00,
        "Parcelas": (1, 36),
        "Taxa": 0.0209,
        "Parentesco": "Flexivel",
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
        "RecebivelMax": 30000.01,
        "Parcelas": (12, 24),
        "Taxa": 0.03,
        "Parentesco": "Profissional",
        "TAC": {"PF": 299.00, "PJ": 299.00},
        "IOF": {"PF": 0.03, "PJ": 0.015}
    },
    {
        "Nome": "Hubcred",
        "Tipos": ["PF"],
        "RecebivelMin": 500.00,
        "RecebivelMax": 30000.01,
        "Parcelas": (12, 24),
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
        "Nome": "Baru",
        "Tipos": ["PF", "PJ"],
        "RecebivelMin": 30000.00,
        "RecebivelMax": 500000.00,
        "Parcelas": (24, 48),
        "Taxa": 0.0259,
        "Parentesco": "Flexivel",
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

# Dados de usuários
USUARIOS = {
    "Cris": "hX730}8S[L",
    "Eduardo": "3(wy81Y9r3",
    "Well": "m0kIr6T)L8",
    "Alvaro": "7lE6#xs3lZ",
    "Dennys" : "t[}3l9#O6$",
    "Raissa": "GC5|2A9p9e",
    "Bruce" : "sHlnU{90]9",
    "Douglas" : "76B/d040/|",
    "Douglas Ogregon" : "1G0pD(^4X?",
    "Earle" : "v9}GPI5-4z",
    "Elton" : "97E1/dp^<<",
    "Fernando" : ")c8Rm+19,^",
    "Fernanda" : "1!9b7DbVj;",
    "Gustavo" : "E/641Q<lN+",
    "João" : "n3FH8@YU62",
    "Levi" : "lR331&8/Lk",
    "Lidy" : "7#24Xhh$+J",
    "Anderson" : "t13Y40@Q<T",
    "Mateus" : "3'552Etelc",
    "Matheus Mendez" : "senhAdm",
    "Naiane" : "osWaS528£[",
    "Omar" : "7H0gLz&2:W",
    "Paulo" : "7E0/Q8a2RE",
    "Renan" : "O8k17h£8J7",
    "Robson" : "0t2Z1_R_k3",
    "Thawan" : "x1K4Ka&08P",
    "Caio": "?c8Rm+19BC",
    "Alessandro": "E/641Q<lN+",
    "Bruna": "n3FH8@YU62",
    "Gabriel": "46V8A{)w/;",
    "Carol": "A!9b7DbVj5",
    "Pedro": "45V8A{)w/;",
    "Rita": "l3FH8iYb55",
    "Rodrigo": "Acdf55#Lp1",
    "Claudionor": "Bcjhf#551",
    "Lai": "Bcjjs2/1",
    "Caique": "Mcd#$15ax!",
    "Wagner": "Hjfh#5879",
    "Amanda": "LpMj587#5",
    "Geisiane": "apoe#5510#"
}

# Inicialização do estado da sessão
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Função para autenticação
def autenticar(username, password):
    if username in USUARIOS and USUARIOS[username] == password:
        return True
    return False

# Página de login
def mostrar_login():
    st.title("🔒 Login do Simulador de Financiamento")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3>Acesso ao Sistema</h3>
            <p>Digite suas credenciais para acessar o simulador financeiro.</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                if autenticar(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login realizado com sucesso!")
                    st.rerun()  # Versão correta em vez de st.experimental_rerun()
                else:
                    st.error("Usuário ou senha incorretos!")

def calcular_parcela(valor_principal, taxa_mensal, tac, iof, parcelas):
    """
    Calcula o valor da parcela usando a fórmula Price correta
    """
    valor_principal = Decimal(str(valor_principal))
    taxa_mensal = Decimal(str(taxa_mensal))
    tac = Decimal(str(tac))
    iof = Decimal(str(iof))
    parcelas = Decimal(str(parcelas))

    # Adiciona TAC ao valor financiado
    valor_financiado = valor_principal + tac

    # Calcula IOF sobre o valor financiado
    valor_com_iof = valor_financiado * (1 + iof)

    # Fator Price
    fator = (taxa_mensal * (1 + taxa_mensal)**parcelas) / ((1 + taxa_mensal)**parcelas - 1)

    # Parcela
    parcela = valor_com_iof * fator
    
    return parcela.quantize(Decimal('0.01'))

def calcular_recebivel(valor_parcela_desejado, taxa_mensal, tac, iof, parcelas):
    """
    Calcula o valor máximo de recebível possível para um valor de parcela desejado
    """
    valor_parcela_desejado = Decimal(str(valor_parcela_desejado))
    taxa_mensal = Decimal(str(taxa_mensal))
    tac = Decimal(str(tac))
    iof = Decimal(str(iof))
    parcelas = Decimal(str(parcelas))

    # Fator Price
    fator = (taxa_mensal * (1 + taxa_mensal)**parcelas) / ((1 + taxa_mensal)**parcelas - 1)
    
    # Calculando o valor com IOF que geraria a parcela desejada
    valor_com_iof = valor_parcela_desejado / fator
    
    # Voltando para descobrir o valor do recebível
    valor_financiado = valor_com_iof / (1 + iof)
    
    # Removendo o TAC para obter o valor do recebível puro
    valor_recebivel = valor_financiado - tac
    
    return valor_recebivel.quantize(Decimal('0.01'))

# Função principal do aplicativo
def mostrar_aplicativo():
    st.title("💰 Simulador de Financiamento Inteligente")
    st.write(f"Bem-vindo(a), {st.session_state.username}!")
    
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()  # Versão correta em vez de st.experimental_rerun()

    st.title("💰 Simulador de Financiamento")
    st.markdown("---")
    
    # Adição da seleção do modo de cálculo
    st.header("🔄 Modo de Cálculo")
    modo_calculo = st.radio(
        "Selecione o modo de cálculo:",
        ["Calcular parcela a partir do valor do recebível", "Calcular recebível a partir do valor da parcela"]
    )

    with st.container():
        st.header("📋 Preencha os Dados da Operação")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if modo_calculo == "Calcular parcela a partir do valor do recebível":
                valor = st.number_input("Recebível (R$)", 
                                  min_value=500.0,
                                  max_value=100000000.0,
                                  step=1000.0,
                                  format="%.2f")
            else:
                valor_parcela_desejada = st.number_input("Valor da Parcela Desejada (R$)", 
                                  min_value=100.0,
                                  max_value=100000.0,
                                  step=100.0,
                                  format="%.2f")
            
        with col2:
            tipo_cliente = st.selectbox("Tipo do Cliente", ["PF", "PJ"])
            
        with col3:
            parentesco = st.selectbox("Destinação do Crédito", 
                                    ["Profissional", "Parentes de 1º Grau", "Flexivel"])

    st.markdown("---")
    with st.container():
        st.header("📅 Condições de Pagamento")
        parcelas = st.number_input("Número de Parcelas", 
                           min_value=1,
                           max_value=60,
                           value=24,
                           help="Selecione o prazo desejado para pagamento")

    resultados = []

    for financeira in FINANCEIRAS:
        try:
            if tipo_cliente not in financeira["Tipos"]:
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
            
            if modo_calculo == "Calcular parcela a partir do valor do recebível":
                # Verificar se o recebível está dentro dos limites da financeira
                if not (financeira["RecebivelMin"] <= valor <= financeira["RecebivelMax"]):
                    continue
                
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
                    "IOF": f"{iof * 100:.1f}%",
                    "Recebível": formatar_moeda(valor)
                })
            else:
                # Novo código para calcular recebível a partir do valor da parcela
                valor_recebivel = calcular_recebivel(
                    valor_parcela_desejado=Decimal(valor_parcela_desejada),
                    taxa_mensal=Decimal(taxa),
                    tac=Decimal(tac),
                    iof=Decimal(iof),
                    parcelas=Decimal(parcelas)
                )
                
                # Verificar se o recebível está dentro dos limites da financeira
                if valor_recebivel < financeira["RecebivelMin"] or valor_recebivel > financeira["RecebivelMax"]:
                    continue
                    
                valor_total = Decimal(valor_parcela_desejada) * parcelas
                
                resultados.append({
                    "Nome": financeira["Nome"],
                    "Taxa": taxa * 100,
                    "Parcela": formatar_moeda(valor_parcela_desejada),
                    "Total": formatar_moeda(valor_total),
                    "TAC": formatar_moeda(tac),
                    "IOF": f"{iof * 100:.1f}%",
                    "Recebível": formatar_moeda(valor_recebivel)
                })
        except Exception as e:
            continue

    st.markdown("---")
    st.header("📊 Resultados das Simulações")

    if resultados:
        # Encontrar melhor e pior parcela
        def parse_valor_parcela(valor_formatado):
            return float(valor_formatado.replace("R$ ", "").replace(".", "").replace(",", "."))
        
        # Determinar qual é a função de comparação com base no modo
        if modo_calculo == "Calcular parcela a partir do valor do recebível":
            # No modo normal, comparamos os valores das parcelas
            parcelas_numericas = [parse_valor_parcela(r['Parcela']) for r in resultados]
            melhor_idx = parcelas_numericas.index(min(parcelas_numericas))
            pior_idx = parcelas_numericas.index(max(parcelas_numericas))
        else:
            # No modo reverso, comparamos os valores dos recebíveis (maior é melhor)
            recebiveis_numericos = [parse_valor_parcela(r['Recebível']) for r in resultados]
            melhor_idx = recebiveis_numericos.index(max(recebiveis_numericos))
            pior_idx = recebiveis_numericos.index(min(recebiveis_numericos))

        # Seção de Melhor/Pior
        col1, col2 = st.columns(2)
        with col1:
            if modo_calculo == "Calcular parcela a partir do valor do recebível":
                st.subheader("🏆 Melhor Oferta (Menor Parcela)")
            else:
                st.subheader("🏆 Melhor Oferta (Maior Recebível)")
                
            melhor = resultados[melhor_idx]
            st.markdown(f"""
            <div class='custom-card' style='border: 2px solid #4CAF50;'>
                <h3 style='color: #4CAF50 !important;'>{melhor['Nome']}</h3>
                <div>📆 Parcelas: <strong>{parcelas}x</strong></div>
                <div>💸 Parcela: <strong style='font-size: 1.2em;'>{melhor['Parcela']}</strong></div>
                <div>💼 Recebível: <strong>{melhor['Recebível']}</strong></div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            if modo_calculo == "Calcular parcela a partir do valor do recebível":
                st.subheader("⚠️ Maior Parcela")
            else:
                st.subheader("⚠️ Menor Recebível")
                
            pior = resultados[pior_idx]
            st.markdown(f"""
            <div class='custom-card' style='border: 2px solid #F44336;'>
                <h3 style='color: #F44336 !important;'>{pior['Nome']}</h3>
                <div>📆 Parcelas: <strong>{parcelas}x</strong></div>
                <div>💸 Parcela: <strong style='font-size: 1.2em;'>{pior['Parcela']}</strong></div>
                <div>💼 Recebível: <strong>{pior['Recebível']}</strong></div>
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
                    badge = "<span style='background: #F44336; color: white; padding: 0.2rem 0.5rem; border-radius: 5px; font-size: 0.8em; margin-left: 0.5rem;'>PIOR</span>"
                
                st.markdown(f"""
                <div class='custom-card'>
                    <h3>{resultado['Nome']}{badge}</h3>
                    <div>
                        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                            <span>📆 Parcelas:</span>
                            <strong>{parcelas}x</strong>
                        </div>
                        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                            <span>💸 Valor Parcela:</span>
                            <strong>{resultado['Parcela']}</strong>
                        </div>
                        <div style='display: flex; justify-content: space-between; margin: 0.5rem 0;'>
                            <span>💼 Recebível:</span>
                            <strong>{resultado['Recebível']}</strong>
                        </div>
                        <hr>
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

# Controle de Fluxo Principal
if not st.session_state.logged_in:
    mostrar_login()
else:
    mostrar_aplicativo()
